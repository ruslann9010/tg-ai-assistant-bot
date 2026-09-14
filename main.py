import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv 
from handlers.handlers import router
from aiogram.client.session.aiohttp import AiohttpSession 
from services.ai_service import AIService
from services import database_db as db_module


logging.basicConfig(level=logging.INFO)

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")

if not API_TOKEN:
    sys.exit("Ошибка: Токен бота не найден! Проверьте файл .env")

async def main():

    session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
    bot = Bot(token=API_TOKEN, session=session) # type: ignore
    dp = Dispatcher()

    ai_service = AIService()

    db_service = db_module.DatabaseService()
    await db_service.init_db()

    # Информационное сообщение
    print("\n🚀 Бот успешно запущен и готов к работе!")
    dp.include_router(router)
    await dp.start_polling(bot, ai_service=ai_service, db_service=db_service)

if __name__ == "__main__":
    asyncio.run(main())
