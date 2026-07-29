"""
Main application entry point.

This module creates the FastAPI application
and registers all API routers.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Collaborative Document Management API",
    description="Backend API for collaborative Word document management.",
    version="1.0.0",
)


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



#def on_login_success(user_info):
    #from app.ui.home import HomePage
    #home_window = HomePage(user_info=user_info, on_open_document=on_document_opened)
    #home_window.resize(900, 700)
    #home_window.show()

#def on_document_opened(doc_name):
   # print(f"→ Ouverture du document : {doc_name}")
   # # ici : instancier document_view.py plus tard