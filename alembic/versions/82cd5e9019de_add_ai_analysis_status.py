"""add AI analysis status

Revision ID: 82cd5e9019de
Revises: 4a0886a35118
Create Date: 2026-08-23 19:26:59.830067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82cd5e9019de'
down_revision: Union[str, Sequence[str], None] = '4a0886a35118'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "analysis_status",
            sa.String(length=20),
            nullable=False,
            server_default="PENDING",
        ),
    )

    op.alter_column(
        "ai_validation_reports",
        "analysis_status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "ai_validation_reports",
        "analysis_status",
    )
