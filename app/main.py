from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth
from app.api import projects
from app.api import documents
from app.api import sections
from app.api.document_lock_queue import router as document_lock_queue_router
from app.api.document_blocks import router as document_block_router


from app.core.exception_handlers import register_exception_handlers

from app.scheduler.lock_queue_scheduler import (
    start_scheduler,
    stop_scheduler,
)
from fastapi import FastAPI

from app.api import auth
from app.api import projects
from app.api import documents
from app.api import sections


from app.core.exception_handlers import register_exception_handlers
from app.api.document_lock_queue import router as document_lock_queue_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="Collaborative Document Management API",
    description="Backend API for collaborative Word document management.",
    version="1.0.0",
    lifespan=lifespan,
)

# API routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)
app.include_router(sections.router)
app.include_router(document_lock_queue_router)
app.include_router(document_block_router)

# Exception handlers
register_exception_handlers(app)


@app.get("/")
def root():
    return {
        "message": "Collaborative Document Management API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

from app.scheduler.lock_queue_scheduler import (
    start_scheduler,
    stop_scheduler,
)