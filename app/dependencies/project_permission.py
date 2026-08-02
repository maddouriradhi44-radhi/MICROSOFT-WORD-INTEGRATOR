from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.database import get_db

from app.models.user import User
from app.models.project_member import ProjectMember
from app.enums.project_role import ProjectRole


def require_project_role(required_role: ProjectRole):

    def role_checker(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        membership = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        ).first()


        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this project."
            )


        if membership.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient project permissions."
            )


        return membership


    return role_checker