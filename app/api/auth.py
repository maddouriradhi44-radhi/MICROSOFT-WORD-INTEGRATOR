"""
Authentication routes.

This module exposes:
- register endpoint
- login endpoint
- current user endpoint
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer

from app.dependencies.database import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
)

from app.services.auth_service import AuthService

from app.utils.jwt_handler import decode_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


 
# REGISTER
 

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return AuthService.register(
        db,
        user
    )



 
# LOGIN
 

@router.post(
    "/login",
    response_model=Token
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):

    return AuthService.login(
        db,
        credentials
    )



 
# CURRENT USER
 

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    # Décoder le JWT
    payload = decode_access_token(token)


    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    email = payload.get("sub")


    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token data"
        )


    return AuthService.get_current_user(
        db,
        email
    )