from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging

settings = get_settings()
setup_logging(debug=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    yield
    # Shutdown actions


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Nurtura AI Co-Parenting & Early Childhood Development Backend API. "
        "Powered by Google Gemini 2.5 Flash for WHO/CDC Milestone Evaluation and Anti-Stunting Smart Plate Vision."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enterprise CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
register_exception_handlers(app)

# Mount API v1 router
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs",
        "api_v1": settings.api_v1_prefix,
    }
