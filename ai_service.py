class AIService:
    """Class responsible for interacting with the AI API (e.g., OpenAI,
    GigaChat, or Ollama).
    """


    def __init__(self) -> None:
        """Initialize the AI client and load required API keys/configurations

        from environment variables.
        """
        # TODO: 1. Получите API-ключ для ИИ из переменных окружения через os.getenv()
        # TODO: 2. Инициализируйте здесь клиент нейросети (когда выберем модель)
        pass



    async def get_response(self, user_text: str) -> str:
        """Sends user text to the AI model and retrieves the generated

        response.

        :param user_text: The message sent by the user in Telegram.
        :return: The textual response from the AI.
        """
         # Подсказка: этот метод ОБЯЗАТЕЛЬНО должен быть асинхронным (async),
        # так как запрос к ИИ через интернет занимает время, и бот не должен зависать.

        # TODO: 3. Напишите здесь временный возврат (return) строки-заглушки,
        # чтобы проверить, что метод вызывается (например, "Тест ИИ: " + user_text)
        return f"Тест ИИ: " + user_text