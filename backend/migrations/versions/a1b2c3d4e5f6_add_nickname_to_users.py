"""add_nickname_to_users

Revision ID: a1b2c3d4e5f6
Revises: 40ec2323705d
Create Date: 2026-05-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '40ec2323705d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nickname', sa.String(length=30), nullable=True))
        batch_op.create_unique_constraint('uq_users_nickname', ['nickname'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_nickname', type_='unique')
        batch_op.drop_column('nickname')
