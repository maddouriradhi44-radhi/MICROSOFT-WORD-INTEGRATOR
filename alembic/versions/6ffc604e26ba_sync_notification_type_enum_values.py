"""sync notification_type enum values

Revision ID: 6ffc604e26ba
Revises: 2c87067b0837
Create Date: 2026-08-09 16:52:17.466521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ffc604e26ba'
down_revision: Union[str, Sequence[str], None] = '2c87067b0837'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    values = [
        "SECURITY", "PROJECT", "DOCUMENT", "SECTION", "COMMENT",
        "MENTION", "VALIDATION", "VERSION", "LOCK", "SCHEDULER", "AI",
    ]
    for value in values:
        op.execute(f"ALTER TYPE notification_type ADD VALUE IF NOT EXISTS '{value}'")


def downgrade() -> None:
    # PostgreSQL ne permet pas de retirer une valeur d'un enum facilement.
    # Downgrade non pris en charge pour cette migration.
    pass