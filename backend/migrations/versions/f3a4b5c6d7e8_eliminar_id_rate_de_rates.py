"""eliminar columna id_rate de la tabla rates

Revision ID: f3a4b5c6d7e8
Revises: e1f2a3b4c5d6
Create Date: 2026-05-29 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f3a4b5c6d7e8'
down_revision = 'e1f2a3b4c5d6'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Eliminar el unique index sobre id_rate (nombre generado automaticamente por MySQL)
    for idx in inspector.get_unique_constraints('rates'):
        if 'id_rate' in idx['column_names']:
            op.drop_constraint(idx['name'], 'rates', type_='unique')

    op.drop_column('rates', 'id_rate')


def downgrade():
    op.add_column('rates', sa.Column('id_rate', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'rates', ['id_rate'])
