"""Fusionar tabla rates en comments: añadir columna rating y eliminar tabla rates

Revision ID: a3b4c5d6e7f8
Revises: f3a4b5c6d7e8
Create Date: 2026-05-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a3b4c5d6e7f8'
down_revision = 'a2b3c4d5e6f7'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Añadir columna solo si no existe (puede que ya exista si la migración se cortó antes)
    columnas = [row[0] for row in conn.execute(sa.text("SHOW COLUMNS FROM comments")).fetchall()]
    if 'rating' not in columnas:
        op.add_column('comments', sa.Column('rating', sa.Integer(), nullable=True))

    # Copiar ratings desde rates hacia comments donde coincidan usuario y juego
    tablas = [row[0] for row in conn.execute(sa.text("SHOW TABLES LIKE 'rates'")).fetchall()]
    if tablas:
        op.execute(sa.text("""
            UPDATE comments c
            JOIN rates r ON r.id_user = c.id_user AND r.id_game_api = c.id_videogame
            SET c.rating = r.rating
        """))

    # Garantizar que no quede ningún NULL
    op.execute(sa.text("UPDATE comments SET rating = 1 WHERE rating IS NULL"))

    # Hacer la columna NOT NULL
    op.alter_column('comments', 'rating', existing_type=sa.Integer(), nullable=False)

    # Eliminar tabla rates si aún existe
    if tablas:
        op.drop_table('rates')


def downgrade():
    # Recrear tabla rates
    op.create_table(
        'rates',
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('id_game_api', sa.Integer(), nullable=False),
        sa.Column('date_rate', sa.Date(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_user', 'id_game_api')
    )

    # Restaurar datos de ratings desde comments
    op.execute("""
        INSERT INTO rates (id_user, id_game_api, date_rate, rating)
        SELECT id_user, id_videogame, date_of_comment, rating
        FROM comments
        WHERE rating IS NOT NULL
    """)

    # Eliminar columna rating de comments
    op.drop_column('comments', 'rating')
