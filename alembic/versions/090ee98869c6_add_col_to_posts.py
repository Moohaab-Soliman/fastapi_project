"""add col to posts

Revision ID: 090ee98869c6
Revises: 64ef4ed4be00
Create Date: 2026-05-05 11:16:28.662538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '090ee98869c6'
down_revision: Union[str, Sequence[str], None] = '64ef4ed4be00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')

    pass
