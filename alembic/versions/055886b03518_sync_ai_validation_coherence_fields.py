"""sync ai validation coherence fields

Revision ID: 055886b03518
Revises: c779d4712d06
Create Date: 2026-08-21 18:59:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "055886b03518"
down_revision: Union[str, Sequence[str], None] = "c779d4712d06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Synchronize the AI validation report coherence fields
    with the SQLAlchemy model.
    """

    # ------------------------------------------------------
    # Remove obsolete column
    # ------------------------------------------------------

    op.drop_column(
        "ai_validation_reports",
        "coherence_analysis",
    )

    # ------------------------------------------------------
    # Add coherence score
    # ------------------------------------------------------

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_score",
            sa.Float(),
            nullable=False,
            server_default="1.0",
        ),
    )

    # ------------------------------------------------------
    # Add coherence level
    # ------------------------------------------------------

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_level",
            sa.String(length=20),
            nullable=False,
            server_default="high",
        ),
    )

    # ------------------------------------------------------
    # Add coherence issues
    # ------------------------------------------------------

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_issues",
            sa.JSON(),
            nullable=True,
        ),
    )

    # ------------------------------------------------------
    # Add coherence summary
    # ------------------------------------------------------

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_summary",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """
    Restore the previous coherence_analysis column.
    """

    # ------------------------------------------------------
    # Remove new coherence fields
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Restore obsolete column
    # ------------------------------------------------------

    op.add_column(
        "ai_validation_reports",
        sa.Column(
            "coherence_analysis",
            sa.JSON(),
            nullable=True,
        ),
    )