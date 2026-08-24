"""update ai section proposals structure

Revision ID: 72225f7c2cfd
Revises: 5222f8f6dd95
Create Date: 2026-08-18 19:01:18.561402

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72225f7c2cfd"
down_revision: Union[str, Sequence[str], None] = "5222f8f6dd95"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "content",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "level",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "order",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.alter_column(
        "ai_section_proposals",
        "section_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "ai_section_proposals",
        "section_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.drop_column(
        "ai_section_proposals",
        "order",
    )

    op.drop_column(
        "ai_section_proposals",
        "level",
    )

    op.drop_column(
        "ai_section_proposals",
        "content",
    )