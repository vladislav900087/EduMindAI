"""remove background jobs

Revision ID: d8969304a0ce
Revises: 5a7026bd5226
Create Date: 2026-08-31 13:21:26.112463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8969304a0ce'
down_revision: Union[str, Sequence[str], None] = '5a7026bd5226'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('background_jobs')


def downgrade() -> None:
    """Downgrade schema."""
    pass
