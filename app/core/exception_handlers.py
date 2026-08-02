"""
Global exception handlers.

This module registers application-wide
exception handlers.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.project import ProjectNotFoundException
from app.exceptions.user import UserNotFoundException
from app.exceptions.permission import PermissionDeniedException


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers.
    """

    @app.exception_handler(ProjectNotFoundException)
    async def project_not_found_handler(
        request: Request,
        exc: ProjectNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_handler(
        request: Request,
        exc: PermissionDeniedException,
    ):
        return JSONResponse(
            status_code=403,
            content={
                "detail": str(exc),
            },
        )