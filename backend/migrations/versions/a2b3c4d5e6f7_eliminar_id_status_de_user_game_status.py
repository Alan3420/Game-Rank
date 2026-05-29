"""eliminar columna id_status de la tabla user_game_status

Revision ID: a2b3c4d5e6f7
Revises: f3a4b5c6d7e8
Create Date: 2026-05-29 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a2b3c4d5e6f7'
down_revision = 'f3a4b5c6d7e8'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    # MySQL no permite MODIFY y DROP COLUMN de la misma columna en una sola sentencia.
    # Se ejecutan tres ALTER TABLE separados:
    # 1. Quitar AUTO_INCREMENT (requisito para poder borrar el UNIQUE KEY)
    bind.execute(sa.text(
        "ALTER TABLE user_game_status MODIFY COLUMN id_status INT NOT NULL"
    ))
    # 2. Borrar el UNIQUE KEY (ahora sin AUTO_INCREMENT ya es posible)
    bind.execute(sa.text(
        "ALTER TABLE user_game_status DROP INDEX uq_status_id"
    ))
    # 3. Eliminar la columna
    bind.execute(sa.text(
        "ALTER TABLE user_game_status DROP COLUMN id_status"
    ))


def downgrade():
    op.add_column('user_game_status', sa.Column('id_status', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'user_game_status', ['id_status'])
