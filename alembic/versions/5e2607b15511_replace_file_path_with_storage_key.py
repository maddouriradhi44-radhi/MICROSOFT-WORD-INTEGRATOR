"""replace file_path with storage_key

Revision ID: 5e2607b15511
Revises: 3b1fa963028d
Create Date: 2026-08-05 00:51:30.358777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e2607b15511'
down_revision: Union[str, Sequence[str], None] = '3b1fa963028d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1) Ajouter temporairement les nouvelles colonnes
    op.add_column(
        'documents',
        sa.Column(
            'storage_key',
            sa.String(length=500),
            nullable=True
        )
    )

    op.add_column(
        'documents',
        sa.Column(
            'original_filename',
            sa.String(length=255),
            nullable=True
        )
    )


    # 2) Copier les anciennes données
    # file_path -> storage_key
    op.execute(
        """
        UPDATE documents
        SET storage_key = file_path
        WHERE file_path IS NOT NULL
        """
    )


    # 3) Générer une valeur pour original_filename
    op.execute(
        """
        UPDATE documents
        SET original_filename = 'unknown.docx'
        WHERE original_filename IS NULL
        """
    )


    # 4) Rendre les colonnes obligatoires
    op.alter_column(
        'documents',
        'storage_key',
        nullable=False
    )

    op.alter_column(
        'documents',
        'original_filename',
        nullable=False
    )


    # 5) Supprimer l'ancien champ
    op.drop_column(
        'documents',
        'file_path'
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        'documents',
        sa.Column(
            'file_path',
            sa.String(length=500),
            nullable=True
        )
    )

    op.execute(
        """
        UPDATE documents
        SET file_path = storage_key
        WHERE storage_key IS NOT NULL
        """
    )

    op.alter_column(
        'documents',
        'file_path',
        nullable=False
    )

    op.drop_column(
        'documents',
        'original_filename'
    )

    op.drop_column(
        'documents',
        'storage_key'
    )