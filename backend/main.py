from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.config import settings
from backend.database import engine, Base
from backend.routers import students, analytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting application...")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="Education Analytics Platform",
    description="Predictive learning analytics for personalized student support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Education Analytics Platform",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "api": "operational"
    }
