"""
Authentication routes.

This module exposes:
- register endpoint
- login endpoint
- current user endpoint
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session



from app.dependencies.database import get_db
from app.dependencies.auth_dependency import get_current_user

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
)

from app.services.auth_service import AuthService

from app.utils.jwt_handler import decode_access_token
from app.schemas.user_schema import ForgotPasswordRequest
from app.schemas.user_schema import ResetPasswordRequest
from app.models.user import User

from app.dependencies.role_dependency import require_role
from app.enums.user_role import UserRole

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



 
# REGISTER
 

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
):

    return AuthService.login(
        db,
        credentials
    )


#LOGOUT

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AuthService.logout(
        db=db,
        user=current_user,
    )

 
# CURRENT USER
 

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/verify-email/{token}")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify user email address.
    """

    return AuthService.verify_email(
        db,
        token
    )

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    return AuthService.forgot_password(
        db,
        data.email
    )

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    return AuthService.reset_password(
        db,
        data.token,
        data.new_password
    )

@router.get("/reset-password/{token}")
def verify_reset_token(
    token: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.reset_token == token
    ).first()


    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )


    if (
        user.reset_token_expires
        and user.reset_token_expires < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=400,
            detail="Reset token expired"
        )


    return {
        "message": "Token valid. You can change your password."
    }

@router.get("/manager-test")
def manager_test(
    current_user = Depends(
        require_role(UserRole.PROJECT_MANAGER)
    )
):
    return {
        "message": "Welcome project manager",
        "user": current_user.email
    }