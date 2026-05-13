"""eliminar_tablas_tierlist

Revision ID: 4da964ba8f03
Revises: b99e4907c1df
Create Date: 2026-05-13 10:29:57.519117

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4da964ba8f03'
down_revision = 'b99e4907c1df'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('tierlist_item')
    op.drop_table('tierlist')


def downgrade():
    op.create_table('tierlist',
    sa.Column('id_tierlist', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_user', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('date_creation', sa.DATE(), nullable=False),
    sa.Column('date_modified', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name=op.f('tierlist_ibfk_1'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_tierlist')
    )
    op.create_table('tierlist_item',
    sa.Column('id_item', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_tierlist', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_game_api', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rank', mysql.VARCHAR(length=1), nullable=False),
    sa.ForeignKeyConstraint(['id_game_api'], ['videoGame.id_game_api'], name=op.f('tierlist_item_ibfk_1'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_tierlist'], ['tierlist.id_tierlist'], name=op.f('tierlist_item_ibfk_2'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_item')
    )