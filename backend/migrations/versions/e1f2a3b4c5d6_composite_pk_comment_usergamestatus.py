"""clave primaria compuesta en comments y user_game_status

Revision ID: e1f2a3b4c5d6
Revises: d0d0e1e2f3a4
Create Date: 2026-05-29 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e1f2a3b4c5d6'
down_revision = 'd0d0e1e2f3a4'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()

    # comments: ampliar PK de (id_comment) a (id_comment, id_videogame)
    bind.execute(sa.text(
        "ALTER TABLE comments DROP PRIMARY KEY, ADD PRIMARY KEY (id_comment, id_videogame)"
    ))

    # user_game_status: cambiar PK de (id_status) a (id_user, id_game_api)
    # En MySQL AUTO_INCREMENT requiere ser parte de un KEY; se quita antes de tocar el PK.
    bind.execute(sa.text(
        "ALTER TABLE user_game_status MODIFY COLUMN id_status INT NOT NULL"
    ))
    bind.execute(sa.text(
        "ALTER TABLE user_game_status DROP PRIMARY KEY, "
        "ADD PRIMARY KEY (id_user, id_game_api), "
        "ADD UNIQUE KEY uq_status_id (id_status)"
    ))
    # Restaurar AUTO_INCREMENT ahora que id_status tiene un UNIQUE KEY
    bind.execute(sa.text(
        "ALTER TABLE user_game_status MODIFY COLUMN id_status INT NOT NULL AUTO_INCREMENT"
    ))


def downgrade():
    bind = op.get_bind()

    # user_game_status: restaurar PK a id_status
    bind.execute(sa.text(
        "ALTER TABLE user_game_status MODIFY COLUMN id_status INT NOT NULL"
    ))
    bind.execute(sa.text(
        "ALTER TABLE user_game_status DROP PRIMARY KEY, "
        "DROP INDEX uq_status_id, "
        "ADD PRIMARY KEY (id_status)"
    ))
    bind.execute(sa.text(
        "ALTER TABLE user_game_status MODIFY COLUMN id_status INT NOT NULL AUTO_INCREMENT"
    ))

    # comments: reducir PK a solo id_comment
    bind.execute(sa.text(
        "ALTER TABLE comments DROP PRIMARY KEY, ADD PRIMARY KEY (id_comment)"
    ))
