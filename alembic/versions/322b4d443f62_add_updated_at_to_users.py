"""add updated_at to users

Revision ID: 322b4d443f62
Revises: a036cef07280
Create Date: 2026-08-01 02:13:14.450487

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "322b4d443f62"
down_revision: Union[str, Sequence[str], None] = "a036cef07280"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade database schema.
    """

    # ============================
    # Create project role ENUM
    # ============================

    project_role_enum = sa.Enum(
        "PROJECT_MANAGER",
        "COLLABORATOR",
        "READER",
        name="project_role"
    )

    project_role_enum.create(
        op.get_bind(),
        checkfirst=True
    )


    # ============================
    # Add role column
    # ============================

    op.add_column(
        "project_members",
        sa.Column(
            "role",
            project_role_enum,
            nullable=True
        )
    )


    # Existing members default role

    op.execute(
        """
        UPDATE project_members
        SET role = 'COLLABORATOR'
        WHERE role IS NULL
        """
    )


    op.alter_column(
        "project_members",
        "role",
        nullable=False
    )


    # ============================
    # Add users.updated_at
    # ============================

    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True
        )
    )


    op.execute(
        """
        UPDATE users
        SET updated_at = NOW()
        """
    )


    op.alter_column(
        "users",
        "updated_at",
        nullable=False
    )


    # ============================
    # Increase verification token
    # ============================

    op.alter_column(
        "users",
        "verification_token",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=512),
        existing_nullable=True
    )


def downgrade() -> None:
    """
    Downgrade database schema.
    """


    op.alter_column(
        "users",
        "verification_token",
        existing_type=sa.String(length=512),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True
    )


    op.drop_column(
        "users",
        "updated_at"
    )


    op.drop_column(
        "project_members",
        "role"
    )


    sa.Enum(
        name="project_role"
    ).drop(
        op.get_bind(),
        checkfirst=True
    )