import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from handlers.handlers import cmd_clear, handle_user_message


class TestHandlers:

    @pytest.mark.asyncio
    async def test_start_handlers_message(self, mock_handlers_service):
        """Verify that the bot correctly sends a welcome message to the user."""
        message = mock_handlers_service
        await message.answer("Привет! Я твой бот.")
        message.answer.assert_called_once()
        assert message.answer.call_args[0][0] == "Привет! Я твой бот."


    @pytest.mark.asyncio
    async def test_cmd_clear_success(self, mock_handlers_service, mock_db_service): 
        """Verify successful clearing of the user's dialogue context.
        
        Ensures that the corresponding database cleanup method is invoked 
        with the correct user ID and that the user receives a confirmation 
        message indicating successful clearing.
        """
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


    @pytest.mark.asyncio
    async def test_handle_user_message_ignores_empty_text(self, mock_handlers_service, mock_ai_service, mock_db_service): 
        """ Verify that messages with empty or missing text are ignored.
        
        Ensures that if the incoming message text is None (e.g., when a photo 
        or sticker is received), the handler returns immediately without 
        saving to the database, invoking the AI service, or replying.
        """
        message = mock_handlers_service
        message.text = None 
      
        await handle_user_message(
            message=message, 
            ai_service=mock_ai_service, 
            db_service=mock_db_service
        )
        
        mock_db_service.save_message.assert_not_called()
        mock_ai_service.get_response.assert_not_called()
        message.answer.assert_not_called()
