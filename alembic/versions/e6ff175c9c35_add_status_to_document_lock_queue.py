"""add status to document lock queue

Revision ID: e6ff175c9c35
Revises: 57cdd0e4a839
Create Date: 2026-08-03 18:45:41.690759

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e6ff175c9c35"
down_revision: Union[str, Sequence[str], None] = "57cdd0e4a839"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    lock_request_status = sa.Enum(
        "WAITING",
        "NOTIFIED",
        "ACCEPTED",
        "REFUSED",
        "EXPIRED",
        name="lockrequeststatus",
    )

    # Create PostgreSQL ENUM type
    lock_request_status.create(
        op.get_bind(),
        checkfirst=True,
    )


    op.add_column(
        "document_lock_queue",
        sa.Column(
            "status",
            lock_request_status,
            nullable=False,
            server_default="WAITING",
        ),
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "document_lock_queue",
        "status",
    )


    lock_request_status = sa.Enum(
        "WAITING",
        "NOTIFIED",
        "ACCEPTED",
        "REFUSED",
        "EXPIRED",
        name="lockrequeststatus",
    )

    lock_request_status.drop(
        op.get_bind(),
        checkfirst=True,
    )