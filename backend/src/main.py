from logging import getLogger
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# from routers.users import router as UsersRouter
# from routers.auth import router as AuthRouter
# from routers.config import router as ConfigRouter
from .auth.controller import router as AuthRouter
from .users.controller import router as UsersRouter
from .config.controller import router as ConfigRouter
from .helpers.db import client

load_dotenv()

# Create Logger
logger = getLogger(__name__)


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
)


# CORS configuration
pricetracker.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


pricetracker.include_router(AuthRouter, tags=["Authentication"])
pricetracker.include_router(UsersRouter, prefix="/users", tags=["Users"])
pricetracker.include_router(ConfigRouter, prefix="/config", tags=["Configuration"])
