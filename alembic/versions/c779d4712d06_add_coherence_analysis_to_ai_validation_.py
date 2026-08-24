"""add coherence analysis to ai validation reports

Revision ID: c779d4712d06
Revises: be56324190e7
Create Date: 2026-08-21 15:55:16.670343

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c779d4712d06"
down_revision: Union[str, Sequence[str], None] = "be56324190e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add coherence analysis fields."""

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_score",
            sa.Float(),
            nullable=False,
            server_default="1.0",
        ),
    )

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_level",
            sa.String(length=20),
            nullable=False,
            server_default="high",
        ),
    )

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_issues",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_summary",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove coherence analysis fields."""

    op.drop_column(
        "ai_validation_reports",
        "coherence_summary",
    )

    op.drop_column(
        "ai_validation_reports",
        "coherence_issues",
    )

    op.drop_column(
        "ai_validation_reports",
        "coherence_level",
    )

    op.drop_column(
        "ai_validation_reports",
        "coherence_score",
    )