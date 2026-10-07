import logging
from logging.config import fileConfig

from alembic import context

# Alembic sin Flask: toma el motor y los modelos de app/database/db.py.
# Uso: alembic -c migrations/alembic.ini upgrade head
from app.database.db import Base, engine
import app.models.User  # noqa: F401  (registran sus tablas en Base.metadata)
import app.models.Comment  # noqa: F401
import app.models.Favorite  # noqa: F401
import app.models.AddFavorite  # noqa: F401

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

target_metadata = Base.metadata


def incluir_objeto(objeto, nombre, tipo, reflejado, comparado_con):
    # La base de Aiven tiene tablas que no son de este backend (friendships,
    # messages...): autogenerate no debe proponer borrarlas
    if tipo == "table" and reflejado and comparado_con is None:
        return False
    return True


def run_migrations_offline():
    url = engine.url.render_as_string(hide_password=False)
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True,
                      include_object=incluir_objeto)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # si autogenerate no detecta cambios no se crea un fichero vacio
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=incluir_objeto,
            process_revision_directives=process_revision_directives,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
