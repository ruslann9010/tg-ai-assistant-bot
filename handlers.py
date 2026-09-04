from ai_service import AIService
from aiogram import Router, types
from aiogram.filters import CommandStart


# TODO: 1. Создайте экземпляр класса Router (например, router = Router())
router = Router()
# Чтобы главный файл main.py мог подключить эти обработчики к диспетчеру.
aiservice = AIService()
# TODO: 2. Создайте экземпляр вашего ИИ-сервиса (например, ai_service = AIService())


# Подсказка: Используйте декоратор вашего роутера для отлавливания команды /start

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handles the /start command.

    Greets the user safely.
    """
    user_name = message.from_user.first_name if message.from_user else "polzovatel"
    await message.answer(f"Привет, {user_name}! Бот успешно запущен!")


# Подсказка: Используйте декоратор роутера без фильтров, чтобы ловить ЛЮБОЙ текст
# @ваш_роутер.message()

@router.message()
async def handle_user_message(message: types.Message):
    """Captures any text message from the user and processes it via

    AIService.
    """
    # TODO: 5. Сделайте проверку: если в сообщении нет текста (message.text равен None),
    # то прервите выполнение функции (return), чтобы бот не падал от картинок или стикеров.

    if not message.text: return

    # TODO: 6. Вызовите метод получения ответа у вашего класса ai_service.
    # Не забудьте передать туда текст пользователя (message.text) и использовать await!

    ai_response = await aiservice.get_response(message.text)

    # TODO: 7. Отправьте полученный от ИИ ответ обратно пользователю в Telegram.
    await message.answer(ai_response)