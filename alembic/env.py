from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.orm.base import Base  # noqa
from app.orm.tables import *

target_metadata = Base.metadata


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_object(object, name, type_, reflected, compare_to):
    # Ignore drop table temporarily
    if type_ == "table" and reflected and compare_to is None:
        return False
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = create_engine(
            config.get_main_option("db_url"),
            poolclass=pool.NullPool,
        )

    connection = connectable.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        process_revision_directives=process_revision_directives,
        compare_type=True,
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    except Exception as exception:
        raise exception
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()