import os
from dotenv import load_dotenv
from gigachat import GigaChat
from dotenv import load_dotenv


load_dotenv()

class AIService:
    """Class responsible for interacting with the AI API (e.g., OpenAI,
    GigaChat, or Ollama).
    """

    def __init__(self) -> None:
        credentials = os.getenv("GIGACHAT_CREDENTIALS") 
        self.client = GigaChat(
            credentials=credentials,
            model="GigaChat-3-Ultra",  
            verify_ssl_certs=False,
            scope="GIGACHAT_API_PERS"
        )

    async def get_response(self, user_text: str) -> str:
        """Sends user text to GigaChat and returns the AI response.

        :param user_text: The message from Telegram user.
        :return: Generated text response from GigaChat.
        """
     
        with self.client as giga:
            response = await giga.achat(user_text)   
            return response.choices[0].message.content
        