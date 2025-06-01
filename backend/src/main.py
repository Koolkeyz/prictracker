import os
from logging import getLogger
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from .auth.controller import router as AuthRouter
from .users.controller import router as UsersRouter
from .config.controller import router as ConfigRouter
from .products.controller import router as ProductsRouter
from .helpers.db import client

load_dotenv()

# Create Logger
logger = getLogger(__name__)

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
        app.state.mongo_client = await client.aconnect()
        logger.info("MongoDB client connected successfully.")
        yield
    finally:
        # Cleanup resources on shutdown
        await app.state.mongo_client.aclose()
        logger.info("MongoDB client disconnected successfully.")
        logger.info("Lifespan context manager finished.")


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


# Mount the frontend build directory
pricetracker.mount(
    "/",
    StaticFiles(directory=site_directory, html=True),
    name="site",
)
