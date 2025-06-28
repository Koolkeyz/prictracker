import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse


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
from .scheduler.scheduling import scheduler

load_dotenv()

# Create Logger
logger = main_logger
environment = get_settings()

# Get the absolute path of the backend directory
backend_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
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
        scheduler.start()
        log_startup_event(logger, "MongoDB client initialized")

        log_startup_event(logger, "Checking for user agents in the database")
        if not await check_if_user_agents_exist():
            log_startup_event(
                logger, "No user agents found", "Adding default user agents"
            )
            await add_user_agents()
            log_startup_event(logger, "Default user agents added successfully")
        else:
            log_startup_event(logger, "User agents already exist in the database")

        log_startup_event(logger, "Checking for admin user in the database")
        if not await check_if_user_exists(environment.ADMIN_USERNAME):
            log_startup_event(
                logger,
                f"Admin user '{environment.ADMIN_USERNAME}' does not exist",
                "Creating admin user",
            )
            await create_user()
            log_startup_event(
                logger,
                f"Admin user '{environment.ADMIN_USERNAME}' created successfully",
            )
        else:
            log_startup_event(
                logger,
                f"Admin user '{environment.ADMIN_USERNAME}' already exists in the database",
            )

        yield
    finally:
        # Cleanup resources on shutdown
        scheduler.shutdown()
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


pricetracker.include_router(AuthRouter, prefix="/api", tags=["Authentication"])
pricetracker.include_router(UsersRouter, prefix="/api/users", tags=["Users"])
pricetracker.include_router(ConfigRouter, prefix="/api/config", tags=["Configuration"])
pricetracker.include_router(ProductsRouter, prefix="/api/products", tags=["Products"])

# Mount the entire site directory as static files (this serves all SvelteKit assets)
pricetracker.mount(
    "/_app",
    StaticFiles(directory=os.path.join(site_directory, "_app")),
    name="static_app",
)


# Serve the root path
@pricetracker.get("/")
async def serve_root():
    return FileResponse(os.path.join(site_directory, "fallback.html"))


# Serve the SPA and its assets
@pricetracker.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Paths that should be handled by the API
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}

    # Check if the requested path is a file in the site directory
    requested_path = os.path.join(site_directory, full_path)
    if os.path.isfile(requested_path):
        return FileResponse(requested_path)

    # For all other paths, return the SPA entry point (fallback.html)
    return FileResponse(os.path.join(site_directory, "fallback.html"))
