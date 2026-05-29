"""eliminar tabla videoGame y FKs asociadas

Revision ID: d0d0e1e2f3a4
Revises: a1b2c3d4e5f6
Create Date: 2026-05-29 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd0d0e1e2f3a4'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


TABLAS_CON_FK = ('favorites', 'rates', 'comments', 'user_game_status')


def upgrade():
    # En MySQL las FKs sin nombre explicito se llaman <tabla>_ibfk_N. Como
    # el sufijo cambia segun el orden de creacion, las detectamos por
    # inspeccion y dropeamos las que apunten a videoGame.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for tabla in TABLAS_CON_FK:
        for fk in inspector.get_foreign_keys(tabla):
            if fk['referred_table'] == 'videoGame':
                op.drop_constraint(fk['name'], tabla, type_='foreignkey')

    op.drop_table('videoGame')


def downgrade():
    op.create_table(
        'videoGame',
        sa.Column('id_game_api', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id_game_api'),
    )
    op.create_foreign_key(
        None, 'favorites', 'videoGame',
        ['id_game_api'], ['id_game_api'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        None, 'rates', 'videoGame',
        ['id_game_api'], ['id_game_api'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        None, 'comments', 'videoGame',
        ['id_videogame'], ['id_game_api'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        None, 'user_game_status', 'videoGame',
        ['id_game_api'], ['id_game_api'], ondelete='CASCADE'
    )
