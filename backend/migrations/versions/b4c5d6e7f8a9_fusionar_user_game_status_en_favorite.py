"""Fusionar tabla user_game_status en favorites: añadir columna status y eliminar tabla user_game_status

Revision ID: b4c5d6e7f8a9
Revises: a3b4c5d6e7f8
Create Date: 2026-05-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b4c5d6e7f8a9'
down_revision = 'a3b4c5d6e7f8'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    columnas = [fila[0] for fila in conn.execute(sa.text("SHOW COLUMNS FROM favorites")).fetchall()]
    if 'status' not in columnas:
        op.add_column('favorites', sa.Column('status', sa.String(length=20), nullable=True))

    tablas = [fila[0] for fila in conn.execute(sa.text("SHOW TABLES LIKE 'user_game_status'")).fetchall()]
    if tablas:
        conn.execute(sa.text("""
            UPDATE favorites f
            JOIN user_game_status ugs
              ON ugs.id_user = f.user_id AND ugs.id_game_api = f.id_game_api
            SET f.status = ugs.status
        """))
        op.drop_table('user_game_status')


def downgrade():
    op.create_table(
        'user_game_status',
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('id_game_api', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_user', 'id_game_api')
    )
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO user_game_status (id_user, id_game_api, status)
        SELECT user_id, id_game_api, status
        FROM favorites
        WHERE status IS NOT NULL
    """))
    op.drop_column('favorites', 'status')
