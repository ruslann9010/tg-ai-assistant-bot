import sys
import pytest
from pathlib import Path
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User  


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from services.database_db import DatabaseService


@pytest.fixture(autouse=True)
def clean_main_import():
    if "main" in sys.modules:
        del sys.modules["main"]
    yield
    if "main" in sys.modules:
        del sys.modules["main"]

@pytest.fixture
def mock_handlers_service():
    mock_user = MagicMock(spec=User, id=12345, first_name="new_user")
    mock_message = AsyncMock(spec=Message)  
    mock_message.from_user = mock_user
    mock_message.answer = AsyncMock()
    return mock_message

@pytest.fixture
def mock_db_service():
    return AsyncMock()

@pytest.fixture
def mock_ai_service():
    """Fixture providing a clean AsyncMock for AIService."""
    return AsyncMock()


@pytest_asyncio.fixture
async def db_service(tmp_path):
    test_db_path = tmp_path / "test_database.db"
    service = DatabaseService(db_path=str(test_db_path))
    await service.init_db()
    yield service
