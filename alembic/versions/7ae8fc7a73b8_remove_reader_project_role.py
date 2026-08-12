"""Remove READER project role

Revision ID: 7ae8fc7a73b8
Revises: 6ffc604e26ba
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7ae8fc7a73b8"
down_revision: Union[str, None] = "6ffc604e26ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # PostgreSQL does not support directly removing
    # a value from an existing ENUM.
    #
    # We therefore recreate the enum without READER.

    op.execute("""
        ALTER TYPE project_role RENAME TO project_role_old;
    """)

    op.execute("""
        CREATE TYPE project_role AS ENUM (
            'PROJECT_MANAGER',
            'COLLABORATOR'
        );
    """)

    op.execute("""
        ALTER TABLE project_members
        ALTER COLUMN role TYPE project_role
        USING role::text::project_role;
    """)

    op.execute("""
        DROP TYPE project_role_old;
    """)


def downgrade() -> None:
    # Recreate the ENUM with READER.

    op.execute("""
        ALTER TYPE project_role RENAME TO project_role_old;
    """)

    op.execute("""
        CREATE TYPE project_role AS ENUM (
            'PROJECT_MANAGER',
            'COLLABORATOR',
            'READER'
        );
    """)

    op.execute("""
        ALTER TABLE project_members
        ALTER COLUMN role TYPE project_role
        USING role::text::project_role;
    """)

    op.execute("""
        DROP TYPE project_role_old;
    """)