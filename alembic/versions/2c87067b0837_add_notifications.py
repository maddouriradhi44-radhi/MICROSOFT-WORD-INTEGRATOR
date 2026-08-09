"""add notifications

Revision ID: 2c87067b0837
Revises: d5aa4a9f6878
Create Date: 2026-08-08 19:58:31.170582
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "2c87067b0837"
down_revision: Union[str, Sequence[str], None] = "d5aa4a9f6878"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ---------------------------------------------------------
    # 1. Create notification_level PostgreSQL ENUM
    # ---------------------------------------------------------
    notification_level = postgresql.ENUM(
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        name="notification_level",
    )

    notification_level.create(
        op.get_bind(),
        checkfirst=True,
    )

    # ---------------------------------------------------------
    # 2. Add title temporarily as nullable
    # ---------------------------------------------------------
    op.add_column(
        "notifications",
        sa.Column(
            "title",
            sa.String(length=150),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 3. Add level temporarily as nullable
    # ---------------------------------------------------------
    op.add_column(
        "notifications",
        sa.Column(
            "level",
            notification_level,
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 4. Add read_at
    # ---------------------------------------------------------
    op.add_column(
        "notifications",
        sa.Column(
            "read_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 5. Add entity information
    # ---------------------------------------------------------
    op.add_column(
        "notifications",
        sa.Column(
            "entity_type",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "notifications",
        sa.Column(
            "entity_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 6. Give existing notifications default values
    # ---------------------------------------------------------
    op.execute(
        """
        UPDATE notifications
        SET title = 'Notification'
        WHERE title IS NULL
        """
    )

    op.execute(
        """
        UPDATE notifications
        SET level = 'INFO'
        WHERE level IS NULL
        """
    )

    # ---------------------------------------------------------
    # 7. Make title and level mandatory
    # ---------------------------------------------------------
    op.alter_column(
        "notifications",
        "title",
        existing_type=sa.String(length=150),
        nullable=False,
    )

    op.alter_column(
        "notifications",
        "level",
        existing_type=notification_level,
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # ---------------------------------------------------------
    # 1. Remove added columns
    # ---------------------------------------------------------
    op.drop_column(
        "notifications",
        "entity_id",
    )

    op.drop_column(
        "notifications",
        "entity_type",
    )

    op.drop_column(
        "notifications",
        "read_at",
    )

    op.drop_column(
        "notifications",
        "level",
    )

    op.drop_column(
        "notifications",
        "title",
    )

    # ---------------------------------------------------------
    # 2. Remove notification_level ENUM
    # ---------------------------------------------------------
    notification_level = postgresql.ENUM(
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        name="notification_level",
    )

    notification_level.drop(
        op.get_bind(),
        checkfirst=True,
    )