import pytest
from unittest.mock import AsyncMock, MagicMock
from unittest.mock import AsyncMock, MagicMock, patch  
from handlers.handlers import cmd_clear, handle_user_message


class TestHandlers:

    @pytest.mark.asyncio
    async def test_cmd_clear_success(self, mock_handlers_service, mock_db_service):  
        await cmd_clear(message=mock_handlers_service, db_service=mock_db_service)
        mock_db_service.clear_context.assert_called_once_with(12345)
        mock_handlers_service.answer.assert_called_once()   
        args, kwargs = mock_handlers_service.answer.call_args
        assert "successfully cleared" in args[0]

    @pytest.mark.asyncio
    async def test_handle_user_message_success(
        self, 
        mock_handlers_service, 
        mock_db_service, 
        mock_ai_service
    ):
        """ Test that handle_user_message successfully processes a text message,
        saves context to the database, requests AI response, and replies to the user.
        """
        mock_handlers_service.text = "Your test prompt here"
        mock_handlers_service.chat = MagicMock(id=999)
        mock_handlers_service.bot = AsyncMock()

        fake_context = [{"role": "user", "content": "Your test prompt here"}]
        mock_db_service.get_context.return_value = fake_context
        mock_ai_service.get_response.return_value = "Your fake AI response"

        with patch("handlers.handlers.ChatActionSender") as mock_sender:
            await handle_user_message(
                message=mock_handlers_service,
                ai_service=mock_ai_service,
                db_service=mock_db_service
            )
        mock_db_service.get_context.assert_called_once_with(user_id=12345, limit=10)
        mock_ai_service.get_response.assert_called_once_with(fake_context)
        mock_handlers_service.answer.assert_called_once_with("Your fake AI response")
        assert mock_db_service.save_message.call_count == 2
   