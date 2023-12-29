"""Main FastAPI application."""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .db import lifespan
from .routers.api import attribution_router, belief_router, factor_router, user_router
from .routers.views import views

app = FastAPI(lifespan=lifespan)

# Could put these in the router module but ... eh
api_router = APIRouter(prefix="/api/v1")
views_router = APIRouter()

api_router.include_router(factor_router.router)
api_router.include_router(attribution_router.router)
api_router.include_router(user_router.router)
api_router.include_router(belief_router.router)
views_router.include_router(views.router)

app.include_router(api_router)
app.include_router(views_router)


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
