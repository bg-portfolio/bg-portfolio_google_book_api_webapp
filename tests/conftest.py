from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI
from typing import Any, Generator
import pytest
import os
import sys
sys.path.insert(0, '../src/')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include src dir in sys.path so that we can import from database/app.py

if 1:  # workaround pep8, vscode autosave
    from src import apis_router
    from src import database
    from src import db_meta


def start_application():
    app = FastAPI()
    # include api routes for testing
    app.include_router(apis_router.api_router)
    return app


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/test_google_book_api"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionTesting = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    db_meta.Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    db_meta.Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture(scope="module")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[database.get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
