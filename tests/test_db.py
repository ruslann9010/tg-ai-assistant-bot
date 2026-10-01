import pytest
from services.database_db import DatabaseService



class TestDataBaseDB:
    @pytest.mark.asyncio
    async def test_save_and_get_context(self, db_service: DatabaseService):
        user_id = 99999
        await db_service.save_message(user_id=user_id, role="user", content="Привет, Бот!")
        await db_service.save_message(user_id=user_id, role="assistant", content="Привет! Чем могу помочь?")
        context = await db_service.get_context(user_id=user_id, limit=10)
        assert len(context) == 2
        assert context[0]["role"] == "user"
        assert context[0]["content"] == "Привет, Бот!"
        assert context[1]["role"] == "assistant"
        assert context[1]["content"] == "Привет! Чем могу помочь?"


    @pytest.mark.asyncio
    async def test_clear_context(self, db_service: DatabaseService):
        user_id = 77777
        await db_service.save_message(user_id=user_id, role="user", content="Удали меня")
        context_before = await db_service.get_context(user_id=user_id)
        assert len(context_before) == 1
        await db_service.clear_context(user_id=user_id)
        context_after = await db_service.get_context(user_id=user_id)
        assert len(context_after) == 0   