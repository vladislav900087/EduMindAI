from sqlalchemy import create_engine, text
from backend.app.core.config import settings

def test_database_connection(db_session):
    result = db_session.execute(text('SELECT 1'))

    assert result.scalar() == 1
