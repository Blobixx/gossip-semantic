import os
import pytest
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.app import app
from app.routers.dependencies import get_db
from factories.Article import ArticleFactory
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import NullPool, create_engine, pool
from sqlalchemy import text
from alembic import command

register(ArticleFactory)

DATABASE_URL_PREFIX = os.getenv("DATABASE_URL_PREFIX", None)
if DATABASE_URL_PREFIX is None:
    raise ValueError("DATABASE_URL_PREFIX environment variable is not set")

DATABASE_NAME = os.getenv("DATABASE_NAME", None)
if DATABASE_NAME is None:
    raise ValueError("DATABASE_NAME environment variable is not set")

ALEMBIC_DATABASE_URL_PREFIX = os.getenv("ALEMBIC_DATABASE_URL_PREFIX", None)
if ALEMBIC_DATABASE_URL_PREFIX is None:
    raise ValueError("ALEMBIC_DATABASE_URL_PREFIX environment variable is not set")

TEST_DATABASE_NAME = os.getenv("TEST_DATABASE_NAME", None)
if TEST_DATABASE_NAME is None:
    raise ValueError("TEST_DATABASE_NAME environment variable is not set")


TEST_DATABASE_URL = f"{ALEMBIC_DATABASE_URL_PREFIX}/{TEST_DATABASE_NAME}"


@pytest.fixture(autouse=True)
def template_db():
    # Connect to the default database to drop/create test database
    engine = create_engine(
        f"{ALEMBIC_DATABASE_URL_PREFIX}/postgres",
        poolclass=NullPool,
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME};"))
        connection.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME};"))

    alembic_config = Config()
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    alembic_config.set_main_option("script_location", "alembic")

    script = ScriptDirectory.from_config(alembic_config)

    # connect to test database
    test_engine = create_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        isolation_level="AUTOCOMMIT",
    )

    with test_engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    # run migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")

    yield


@pytest.fixture(autouse=True)
def db_session(template_db):
    engine = create_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
    )

    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db_dependency(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def article_factory(db_session):
    class _ArticleFactory(ArticleFactory):
        class Meta:
            sqlalchemy_session = db_session

    return _ArticleFactory
