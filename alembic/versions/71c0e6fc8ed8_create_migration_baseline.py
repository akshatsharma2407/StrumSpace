"""create migration baseline

Revision ID: 71c0e6fc8ed8
Revises: 
Create Date: 2026-11-25 22:32:29.669508

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '71c0e6fc8ed8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
