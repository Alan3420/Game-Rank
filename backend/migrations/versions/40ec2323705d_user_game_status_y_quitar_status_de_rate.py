"""user_game_status_y_quitar_status_de_rate

Revision ID: 40ec2323705d
Revises: 4da964ba8f03
Create Date: 2026-05-13 10:56:10.623306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '40ec2323705d'
down_revision = '4da964ba8f03'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_game_status',
        sa.Column('id_status', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('id_game_api', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['id_game_api'], ['videoGame.id_game_api'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_status')
    )

    with op.batch_alter_table('rates', schema=None) as batch_op:
        batch_op.drop_column('status')


def downgrade():
    with op.batch_alter_table('rates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', mysql.VARCHAR(length=20), nullable=True))

    op.drop_table('user_game_status')