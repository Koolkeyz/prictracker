import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from .auth.controller import router as AuthRouter
from .users.controller import router as UsersRouter
from .config.controller import router as ConfigRouter
from .products.controller import router as ProductsRouter
from .helpers.db import client
from .helpers.logger import main_logger, log_startup_event, log_request
from .helpers.seed import (
    add_user_agents,
    check_if_user_agents_exist,
    check_if_user_exists,
    create_user,
)
from .helpers.settings import get_settings

load_dotenv()

# Create Logger
logger = main_logger
environment = get_settings()

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(os.path.dirname(backend_dir), "frontend")
site_directory = os.path.join(backend_dir, "site")
static_directory = os.path.join(backend_dir, "static")




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This can be used to initialize resources or perform startup tasks.
    """
    try:
        # Initialize the MongoDB client
        app.state.mongo_client = client
        await app.state.mongo_client.aconnect()
        # Note: AsyncMongoClient doesn't have aconnect() method
        # It connects automatically when a query is executed
        log_startup_event(logger, "MongoDB client initialized")
        
        log_startup_event(logger, "Checking for user agents in the database")
        if not await check_if_user_agents_exist():
            log_startup_event(logger, "No user agents found", "Adding default user agents")
            await add_user_agents()
            log_startup_event(logger, "Default user agents added successfully")
        else:
            log_startup_event(logger, "User agents already exist in the database")
        
        log_startup_event(logger, "Checking for admin user in the database")
        if not await check_if_user_exists(environment.ADMIN_USERNAME):
            log_startup_event(
                logger, 
                f"Admin user '{environment.ADMIN_USERNAME}' does not exist", 
                "Creating admin user"
            )
            await create_user()
            log_startup_event(
                logger, 
                f"Admin user '{environment.ADMIN_USERNAME}' created successfully"
            )
        else:
            log_startup_event(
                logger, 
                f"Admin user '{environment.ADMIN_USERNAME}' already exists in the database"
            )

        yield
    finally:
        # Cleanup resources on shutdown
        await app.state.mongo_client.aclose()
        log_startup_event(logger, "MongoDB client disconnected successfully")
        log_startup_event(logger, "Application shutdown complete")


pricetracker = FastAPI(
    title="PriceTracker API",
    description="API for PriceTracker, a web application that tracks product prices across Amazon and Newegg.",
    debug=True,
    version="0.0.1",
    lifespan=lifespan,
)


# CORS configuration
pricetracker.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:5173"
        "*"
    ],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Request logging middleware
@pricetracker.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all HTTP requests in uvicorn style.
    """
    start_time = time.time()
    
    # Skip logging for static files and health checks
    if request.url.path.startswith(("/static", "/favicon", "/_app")):
        response = await call_next(request)
        return response
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log the request
    log_request(
        logger=main_logger,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time=process_time,
        client_ip=client_ip
    )
    
    return response


pricetracker.include_router(AuthRouter, prefix="/api", tags=["Authentication"])
pricetracker.include_router(UsersRouter, prefix="/api/users", tags=["Users"])
pricetracker.include_router(ConfigRouter, prefix="/api/config", tags=["Configuration"])
pricetracker.include_router(ProductsRouter, prefix="/api/products", tags=["Products"])


# Mount the frontend build directory
pricetracker.mount(
    "/",
    StaticFiles(directory=site_directory, html=True),
    name="site",
)
