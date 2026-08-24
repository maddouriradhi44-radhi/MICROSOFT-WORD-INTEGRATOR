"""add status to ai section proposals

Revision ID: add_ai_proposal_status
Revises: c8292db73b0a
Create Date: 2026-08-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_ai_proposal_status"
down_revision: Union[str, Sequence[str], None] = "c8292db73b0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    proposal_status = sa.Enum(
        "PENDING",
        "ACCEPTED",
        "REJECTED",
        name="ai_proposal_status",
    )

    proposal_status.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "ai_section_proposals",
        sa.Column(
            "status",
            proposal_status,
            nullable=False,
            server_default="PENDING",
        ),
    )

    op.alter_column(
        "ai_section_proposals",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "ai_section_proposals",
        "status",
    )

    sa.Enum(
        "PENDING",
        "ACCEPTED",
        "REJECTED",
        name="ai_proposal_status",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )