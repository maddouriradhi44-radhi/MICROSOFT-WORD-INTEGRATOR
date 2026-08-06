"""add versioning support

Revision ID: 0104f53de8aa
Revises: 21e3549fe8db
Create Date: 2026-08-06 02:10:24.997687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0104f53de8aa'
down_revision: Union[str, Sequence[str], None] = '21e3549fe8db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    version_change_type = sa.Enum(
        'CREATE',
        'UPDATE',
        'RESTORE',
        'IMPORT',
        name='version_change_type'
    )

    version_change_type.create(
        op.get_bind(),
        checkfirst=True
    )

    # Add new version fields
    op.add_column(
        'versions',
        sa.Column(
            'title_snapshot',
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        'versions',
        sa.Column(
            'content_snapshot',
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        'versions',
        sa.Column(
            'change_comment',
            sa.String(length=500),
            nullable=True
        )
    )

    op.add_column(
        'versions',
        sa.Column(
            'is_current',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        'versions',
        sa.Column(
            'change_type',
            sa.Enum(
                'CREATE',
                'UPDATE',
                'RESTORE',
                'IMPORT',
                name='version_change_type'
            ),
            nullable=False,
            server_default='UPDATE'
        )
    )

    op.add_column(
        'versions',
        sa.Column(
            'parent_version_id',
            sa.Integer(),
            nullable=True
        )
    )


    # Copy old content into new snapshot field
    op.execute(
        """
        UPDATE versions
        SET content_snapshot = content
        """
    )


    # Self reference relation
    op.create_foreign_key(
        None,
        'versions',
        'versions',
        ['parent_version_id'],
        ['id']
    )


    # Remove old fields
    op.drop_column(
        'versions',
        'content'
    )

    op.drop_column(
        'versions',
        'validation_status'
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('versions', sa.Column('validation_status', postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='validation_status'), autoincrement=False, nullable=False))
    op.add_column('versions', sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'versions', type_='foreignkey')
    op.drop_column('versions', 'parent_version_id')
    op.drop_column('versions', 'change_type')
    op.drop_column('versions', 'is_current')
    op.drop_column('versions', 'change_comment')
    op.drop_column('versions', 'title_snapshot')

    version_change_type = postgresql.ENUM(
        'CREATE',
        'UPDATE',
        'RESTORE',
        'IMPORT',
        name='version_change_type'
    )
    version_change_type.drop(
        op.get_bind(),
        checkfirst=True
    )