"""add modified ai proposal status

Revision ID: 4a0886a35118
Revises: 6c5f823ccf0b
Create Date: 2026-08-23 15:09:04.391078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a0886a35118'
down_revision: Union[str, Sequence[str], None] = '6c5f823ccf0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE ai_proposal_status ADD VALUE IF NOT EXISTS 'MODIFIED'"
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
