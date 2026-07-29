"""
Main application entry point.

This module creates the FastAPI application
and registers all API routers.
"""

from fastapi import FastAPI

from app.api import auth

app = FastAPI(
    title="Collaborative Document Management API",
    description="Backend API for collaborative Word document management.",
    version="1.0.0",
)

app.include_router(auth.router)


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