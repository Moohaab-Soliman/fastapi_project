"""add posts cols

Revision ID: aa7ead794e19
Revises: dde1fedd56a1
Create Date: 2026-05-05 13:21:17.525061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7ead794e19'
down_revision: Union[str, Sequence[str], None] = 'dde1fedd56a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False, server_default='TRUE' ))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default='now()'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    """Downgrade schema."""
    pass
