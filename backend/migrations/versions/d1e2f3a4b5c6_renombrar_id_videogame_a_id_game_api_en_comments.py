"""renombrar id_videogame a id_game_api en comments y simplificar PK

Revision ID: d1e2f3a4b5c6
Revises: c0d1e2f3a4b5
Create Date: 2026-05-31

"""
from alembic import op
import sqlalchemy as sa


revision = 'd1e2f3a4b5c6'
down_revision = 'c0d1e2f3a4b5'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text(
        "ALTER TABLE comments "
        "CHANGE COLUMN id_videogame id_game_api INT NOT NULL, "
        "DROP PRIMARY KEY, "
        "ADD PRIMARY KEY (id_comment)"
    ))


def downgrade():
    op.execute(sa.text(
        "ALTER TABLE comments "
        "CHANGE COLUMN id_game_api id_videogame INT NOT NULL, "
        "DROP PRIMARY KEY, "
        "ADD PRIMARY KEY (id_comment, id_videogame)"
    ))
