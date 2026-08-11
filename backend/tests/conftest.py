import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.database import Base

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
