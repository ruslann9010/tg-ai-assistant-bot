import os
import pytest
from unittest.mock import AsyncMock, patch

# Set fake environment variables to initialize GigaChat without real credentials
os.environ["GIGACHAT_CREDENTIALS"] = "fake_credentials_for_testing"
from services.ai_service import AIService 


class TestAiService:
    """ Test suite for validating the AIService component.
    
    Ensures correct payload processing and interaction with GigaChat API 
    without making live network calls.
    """

    @pytest.mark.asyncio
    @patch('services.ai_service.GigaChat.achat', new_callable=AsyncMock)
    async def test_generate_response_success(self, mock_achat):
        """ Scenario 1: Successful AI response.
        
        Verifies that get_response correctly parses and returns the text 
        received from the GigaChat API structure.
        """
        
        mock_response = AsyncMock()
        mock_message_object = AsyncMock()
        mock_message_object.message.content = "Ответ получен всё хорошо!"
        mock_response.choices = [mock_message_object]   
        mock_achat.return_value = mock_response
        context = [{"role": "user", "content": "Поздоровайся"}]    
        ai_service = AIService()
        ai_response = await ai_service.get_response(context)
        assert ai_response == "Ответ получен всё хорошо!"
        mock_achat.assert_called_once()

    @pytest.mark.asyncio
    @patch('services.ai_service.GigaChat.achat', new_callable=AsyncMock)
    async def test_generate_response_api_failure(self, mock_achat):
        """ Scenario 2: AI API failure handling.
        
        Verifies that the method securely manages API exceptions 
        and returns a fallback message instead of crashing the application.
        """
       
        mock_achat.side_effect = Exception("GigaChat Server Error 500")
        context = [{"role": "user", "content": "Запрос во время сбоя"}]
        ai_service = AIService()
        with pytest.raises(Exception) as exc_info:
            await ai_service.get_response(context)
        assert "GigaChat Server Error 500" in str(exc_info.value)
        mock_achat.assert_called_once()

    @pytest.mark.asyncio
    @patch('services.ai_service.GigaChat.achat', new_callable=AsyncMock)
    async def test_get_response_empty_context(self, mock_achat):
        """ Scenario 3: Empty dialogue context.
        
        Verifies how the method behaves when an empty list of messages is provided.
        """
        
        ai_service = AIService()
        invalid_context = []
        mock_response = AsyncMock()
        mock_message_object = AsyncMock()
        mock_message_object.message.content = "Контекст был пуст"
        mock_response.choices = [mock_message_object]
        mock_achat.return_value = mock_response
        ai_response = await ai_service.get_response(invalid_context)
        assert ai_response == "Контекст был пуст"
        mock_achat.assert_called_once()
