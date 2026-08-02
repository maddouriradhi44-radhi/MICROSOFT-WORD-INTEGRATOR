"""
Main application entry point.

This module creates the FastAPI application
and registers all API routers.
"""

from fastapi import FastAPI

from app.api import auth
from app.api import projects

from app.core.exception_handlers import register_exception_handlers


app = FastAPI(
    title="Collaborative Document Management API",
    description="Backend API for collaborative Word document management.",
    version="1.0.0",
)


# API routers
app.include_router(auth.router)
app.include_router(projects.router)


# Exception handlers
register_exception_handlers(app)


@app.get("/")
def root():
    """
    Root endpoint.
    """
    return {
        "message": "Collaborative Document Management API is running."
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy"
    }