from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth
from app.api import projects
from app.api import documents
from app.api import sections
from app.api import versions
from app.api import comment
from app.api.validation import router as validation_router
from app.api.document_lock_queue import (
    router as document_lock_queue_router,
)

from app.api.document_blocks import (
    router as document_block_router,
)

from app.core.exception_handlers import (
    register_exception_handlers,
)

from app.scheduler.lock_queue_scheduler import (
    start_scheduler,
    stop_scheduler,
)

from app.api.notification import router as notification_router

from app.api import audit


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


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)
app.include_router(sections.router)
app.include_router(document_lock_queue_router)
app.include_router(document_block_router)
app.include_router(versions.router)
app.include_router(comment.router)
app.include_router(notification_router)
app.include_router(audit.router)
register_exception_handlers(app)
app.include_router(validation_router)



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