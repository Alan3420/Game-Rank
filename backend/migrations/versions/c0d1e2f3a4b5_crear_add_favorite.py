"""Crear tabla add_favorite: interrelacion N:M agregar entre usuarios y favoritos

Revision ID: c0d1e2f3a4b5
Revises: b4c5d6e7f8a9
Create Date: 2026-05-30 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c0d1e2f3a4b5'
down_revision = 'b4c5d6e7f8a9'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1. Crear tabla add_favorite si no existe
    tablas = [f[0] for f in conn.execute(sa.text("SHOW TABLES LIKE 'add_favorite'")).fetchall()]
    if not tablas:
        op.create_table(
            'add_favorite',
            sa.Column('fav_id',     sa.Integer(), nullable=False),
            sa.Column('id_user',    sa.Integer(), nullable=False),
            sa.Column('date_added', sa.Date(),    nullable=False),
            sa.ForeignKeyConstraint(['fav_id'],  ['favorites.fav_id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['id_user'], ['users.id_user'],    ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('fav_id', 'id_user')
        )

        # 2. Migrar datos existentes desde favorites
        conn.execute(sa.text("""
            INSERT INTO add_favorite (fav_id, id_user, date_added)
            SELECT fav_id, user_id, COALESCE(date_added, CURDATE())
            FROM favorites
            WHERE user_id IS NOT NULL
        """))

    # 3. Obtener y eliminar FK de user_id en favorites
    fk_rows = conn.execute(sa.text("""
        SELECT CONSTRAINT_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'favorites'
          AND COLUMN_NAME = 'user_id'
          AND REFERENCED_TABLE_NAME IS NOT NULL
    """)).fetchall()

    for row in fk_rows:
        conn.execute(sa.text(f"ALTER TABLE favorites DROP FOREIGN KEY `{row[0]}`"))

    # 4. Reconstruir PK de favorites como solo fav_id (eliminar user_id e id_game_api del PK)
    columnas_pk = [r[0] for r in conn.execute(sa.text("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'favorites'
          AND CONSTRAINT_NAME = 'PRIMARY'
        ORDER BY ORDINAL_POSITION
    """)).fetchall()]

    if set(columnas_pk) != {'fav_id'}:
        conn.execute(sa.text(
            "ALTER TABLE favorites DROP PRIMARY KEY, ADD PRIMARY KEY (fav_id)"
        ))

    # 5. Eliminar columnas user_id y date_added de favorites
    columnas = [f[0] for f in conn.execute(sa.text("SHOW COLUMNS FROM favorites")).fetchall()]

    if 'user_id' in columnas:
        op.drop_column('favorites', 'user_id')

    if 'date_added' in columnas:
        op.drop_column('favorites', 'date_added')


def downgrade():
    conn = op.get_bind()

    # 1. Volver a añadir user_id y date_added a favorites
    columnas = [f[0] for f in conn.execute(sa.text("SHOW COLUMNS FROM favorites")).fetchall()]

    if 'user_id' not in columnas:
        op.add_column('favorites', sa.Column('user_id', sa.Integer(), nullable=True))

    if 'date_added' not in columnas:
        op.add_column('favorites', sa.Column('date_added', sa.Date(), nullable=True))

    # 2. Recuperar datos desde add_favorite
    conn.execute(sa.text("""
        UPDATE favorites f
        JOIN add_favorite af ON af.fav_id = f.fav_id
        SET f.user_id = af.id_user,
            f.date_added = af.date_added
    """))

    # 3. Hacer user_id NOT NULL y reconstruir PK compuesta
    op.alter_column('favorites', 'user_id',
                    existing_type=sa.Integer(), nullable=False)
    op.alter_column('favorites', 'date_added',
                    existing_type=sa.Date(), nullable=False)

    conn.execute(sa.text(
        "ALTER TABLE favorites DROP PRIMARY KEY, ADD PRIMARY KEY (fav_id, user_id, id_game_api)"
    ))

    # 4. Restaurar FK de user_id
    op.create_foreign_key(
        None, 'favorites', 'users',
        ['user_id'], ['id_user'],
        ondelete='CASCADE'
    )

    # 5. Eliminar tabla add_favorite
    op.drop_table('add_favorite')
