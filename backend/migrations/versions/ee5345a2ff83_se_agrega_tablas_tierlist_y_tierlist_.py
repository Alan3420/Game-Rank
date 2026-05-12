"""se agrega tablas tierlist y tierlist_item

Revision ID: ee5345a2ff83
Revises: 05db1cca8436
Create Date: 2026-05-13 00:36:34.411415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee5345a2ff83'
down_revision = '05db1cca8436'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tierlist',
        sa.Column('id_tierlist', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('date_creation', sa.Date(), nullable=False),
        sa.Column('date_modified', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_tierlist')
    )
    op.create_table('tierlist_item',
        sa.Column('id_item', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_tierlist', sa.Integer(), nullable=False),
        sa.Column('id_game_api', sa.Integer(), nullable=False),
        sa.Column('rank', sa.String(length=1), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_game_api'], ['videoGame.id_game_api'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_tierlist'], ['tierlist.id_tierlist'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_item')
    )


def downgrade():
    op.drop_table('tierlist_item')
    op.drop_table('tierlist')