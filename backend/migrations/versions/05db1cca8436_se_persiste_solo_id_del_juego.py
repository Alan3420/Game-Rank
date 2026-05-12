"""se persiste solo id del juego

Revision ID: 05db1cca8436
Revises: c864598bf75c
Create Date: 2026-05-12 14:20:33.841017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '05db1cca8436'
down_revision = 'c864598bf75c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('videoGame', schema=None) as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('date_release')
        batch_op.drop_column('platforms')
        batch_op.drop_column('development_company')


def downgrade():
    with op.batch_alter_table('videoGame', schema=None) as batch_op:
        batch_op.add_column(sa.Column('development_company', mysql.VARCHAR(length=255), nullable=False))
        batch_op.add_column(sa.Column('platforms', mysql.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('date_release', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=255), nullable=False))