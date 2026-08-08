"""Add comments support

Revision ID: e26a6c93d166
Revises: 35c61b1fdf28
Create Date: ...
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e26a6c93d166"
down_revision = "35c61b1fdf28"
branch_labels = None
depends_on = None


def upgrade() -> None:
    comment_status = sa.Enum(
        "OPEN",
        "RESOLVED",
        name="comment_status",
    )

    comment_status.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "comments",
        sa.Column(
            "status",
            comment_status,
            nullable=False,
            server_default="OPEN",
        ),
    )

    op.alter_column(
        "comments",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "comments",
        "status",
    )

    sa.Enum(
        "OPEN",
        "RESOLVED",
        name="comment_status",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )