"""add ai proposal review fields

Revision ID: 13b396370d2b
Revises: add_ai_proposal_status
Create Date: 2026-08-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "13b396370d2b"
down_revision: Union[str, Sequence[str], None] = "add_ai_proposal_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add Project Manager review fields."""

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "reviewed_by",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_ai_section_proposals_reviewed_by_users",
        "ai_section_proposals",
        "users",
        ["reviewed_by"],
        ["id"],
    )

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "reviewed_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "review_comment",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove Project Manager review fields."""

    op.drop_column(
        "ai_section_proposals",
        "review_comment",
    )

    op.drop_column(
        "ai_section_proposals",
        "reviewed_at",
    )

    op.drop_constraint(
        "fk_ai_section_proposals_reviewed_by_users",
        "ai_section_proposals",
        type_="foreignkey",
    )

    op.drop_column(
        "ai_section_proposals",
        "reviewed_by",
    )