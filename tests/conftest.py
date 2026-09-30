import sys
import pytest
from pathlib import Path
import pytest_asyncio


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from services.database_db import DatabaseService

@pytest.fixture(scope="session")
def event_loop_policy():
    import asyncio
    return asyncio.get_event_loop_policy()

@pytest_asyncio.fixture
async def db_service(tmp_path):
    test_db_path = tmp_path / "test_database.db"
    service = DatabaseService(db_path=str(test_db_path))
    await service.init_db()
    yield service