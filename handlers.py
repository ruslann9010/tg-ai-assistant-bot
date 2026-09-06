from ai_service import AIService
from aiogram import Router, types
from aiogram.filters import CommandStart


router = Router()
aiservice = AIService()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handles the /start command.

    Greets the user safely.
    """
    user_name = message.from_user.first_name if message.from_user else "polzovatel"
    await message.answer(f"Привет, {user_name}! Бот успешно запущен!")


@router.message()
async def handle_user_message(message: types.Message):
    """Captures any text message from the user and processes it via

    AIService.
    """
    if not message.text: return
    ai_response = await aiservice.get_response(message.text)
    await message.answer(ai_response)