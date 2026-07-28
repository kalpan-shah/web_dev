"""fix user table last accessed server default

Revision ID: 1ac631b0884f
Revises: 6b70e3a53fee
Create Date: 2026-07-28 10:33:03.388756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ac631b0884f'
down_revision: Union[str, Sequence[str], None] = '6b70e3a53fee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users', 
        'last_accessed', 
        existing_type=sa.DateTime(timezone=True), 
        existing_nullable=False,
        server_default=sa.text('now()')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users', 
        'last_accessed', 
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=None
    )
