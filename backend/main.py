from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import router as UsersRouter

load_dotenv()
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

@pricetracker.get("/login", tags=["Authentication"])
async def login():
    return {"message": "Login endpoint is not implemented yet."}

pricetracker.include_router(UsersRouter, prefix="/users", tags=["Users"])
