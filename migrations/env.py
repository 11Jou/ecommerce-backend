from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from Core.settings import get_database_url
from Core.Database import Base

# Import every model module so their tables register on Base.metadata.
# Add new model modules here as you create them.
import Modules.Auth.Models  # noqa: F401
import Modules.Stock.Models  # noqa: F401
import Modules.Order.Models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = get_database_url()
print("DATABASE_URL: ", DATABASE_URL)


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
