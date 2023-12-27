"""Main FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .db import db
from .routers.api import attribution_router, belief_router, factor_router, user_router
from .routers.views import views


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(factor_router.router)
app.include_router(attribution_router.router)
app.include_router(user_router.router)
app.include_router(belief_router.router)
app.include_router(views.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="static/templates") - these are loaded in the views.py file

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
