"""Se agrega cascada de eliminacion en Rate y Favorite

Revision ID: c864598bf75c
Revises: 2008b9a14636
Create Date: 2026-05-10 00:30:12.464977

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c864598bf75c'
down_revision = '2008b9a14636'
branch_labels = None
depends_on = None


def upgrade():
    # Nota: se eliminaron los drop_index() autogenerados porque MySQL los
    # necesita para los FKs. Solo aplicamos el cambio de FKs a CASCADE.
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('favorites_ibfk_2'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('favorites_ibfk_1'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'videoGame', ['id_game_api'], ['id_game_api'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id_user'], ondelete='CASCADE')

    with op.batch_alter_table('rates', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('rates_ibfk_2'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('rates_ibfk_1'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'videoGame', ['id_game_api'], ['id_game_api'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'users', ['id_user'], ['id_user'], ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('rates', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('rates_ibfk_1'), 'users', ['id_user'], ['id_user'])
        batch_op.create_foreign_key(batch_op.f('rates_ibfk_2'), 'videoGame', ['id_game_api'], ['id_game_api'])

    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('favorites_ibfk_1'), 'users', ['user_id'], ['id_user'])
        batch_op.create_foreign_key(batch_op.f('favorites_ibfk_2'), 'videoGame', ['id_game_api'], ['id_game_api'])
