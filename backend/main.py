from dotenv import load_dotenv
from fastapi import FastAPI
from routers.users import router as UsersRouter

load_dotenv()
app = FastAPI(
    title="PriceTracker API",
    description="API for PriceTracker, a web application that tracks product prices across Amazon and Newegg.",
    debug=True,
    version="0.0.1",
)

app.include_router(UsersRouter, prefix="/users", tags=["Users"])
