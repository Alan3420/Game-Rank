"""tierlist_item_sin_position

Revision ID: b99e4907c1df
Revises: ee5345a2ff83
Create Date: 2026-05-13 09:50:01.487195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b99e4907c1df'
down_revision = 'ee5345a2ff83'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('tierlist_item', schema=None) as batch_op:
        batch_op.drop_column('position')


def downgrade():
    with op.batch_alter_table('tierlist_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position', mysql.INTEGER(), autoincrement=False, nullable=False))