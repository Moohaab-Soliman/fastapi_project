"""add foreign key to posts table 


Revision ID: dde1fedd56a1
Revises: 66220058bc50
Create Date: 2026-05-05 11:50:45.332338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKeyConstraint

# revision identifiers, used by Alembic.
revision: str = 'dde1fedd56a1'
down_revision: Union[str, Sequence[str], None] = '66220058bc50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id', sa.Integer(),  nullable=False))
    op.create_foreign_key('post_owner_fk',source_table='posts',referent_table='users',local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_owner_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
