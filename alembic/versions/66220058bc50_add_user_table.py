"""add user table

Revision ID: 66220058bc50
Revises: 090ee98869c6
Create Date: 2026-05-05 11:30:56.298380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = '66220058bc50'
down_revision: Union[str, Sequence[str], None] = '090ee98869c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('email', sa.String(), nullable=False,unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    """Downgrade schema."""
    pass
