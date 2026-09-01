import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.database import Base

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import get_db

@pytest.fixture
def test_engine():
    engine = create_engine(settings.test_database_url)

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()




    


