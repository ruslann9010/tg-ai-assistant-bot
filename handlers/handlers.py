from services.ai_service import AIService
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction


router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handles the /start command.

    Greets the user safely.
    """
    user_name = message.from_user.first_name if message.from_user else "polzovatel"
    await message.answer(f"Привет, {user_name}! Бот успешно запущен!")



@router.message(Command("clear"))
async def cmd_clear(message: types.Message, db_service):
    """Handles the /clear command to reset the user's conversation memory.

    Verifies the existence of the user object, purges their entire chat 
    history from the persistence layer via DatabaseService, and dispatches 
    a confirmation message to notify the user that their context has been reset.

    Args:
        message (types.Message): The inbound Telegram message object instance.
        db_service (DatabaseService): The dependency-injected database 
            service wrapper.
    """

    if not message.from_user:
        return
    await db_service.clear_context(message.from_user.id)
    await message.answer("🧹 History of our dialogue has been successfully cleared! We can start with a clean slate.")



@router.message()
async def handle_user_message(message: types.Message, ai_service: AIService, db_service):
    """Captures any text message from the user, saves it to DB, 
    
    and processes context via AIService."""

    if not message.text or not message.from_user: 
        return
    
    user_id = message.from_user.id
    await db_service.save_message(user_id=user_id, role="user", content=message.text)
    context = await db_service.get_context(user_id=user_id, limit=10)
    async with ChatActionSender(bot=message.bot, chat_id=message.chat.id, action=ChatAction.TYPING): # type: ignore
        ai_response = await ai_service.get_response(context)    
    await db_service.save_message(user_id=user_id, role="assistant", content=ai_response)  
    await message.answer(ai_response)





