import os
import sys
import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv 
from handlers.handlers import router
from aiogram.client.session.aiohttp import AiohttpSession 
from aiogram.exceptions import TelegramUnauthorizedError
from services.ai_service import AIService
from services import database_db as db_module


logging.basicConfig(level=logging.INFO)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")

if not BOT_TOKEN:
    sys.exit("Ошибка: Токен бота не найден! Проверьте файл .env")


async def check_proxy(proxy_url: str) -> bool:
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("https://telegram.org", proxy=proxy_url) as resp:
                return resp.status == 200
    except Exception:
        return False 

async def main():

    if PROXY_URL:
        is_valid = await check_proxy(PROXY_URL)
        if not is_valid:
            sys.exit(f"❌ Ошибка: Указанный PROXY_URL ({PROXY_URL}) не работает или недоступен!")
        print("✅ Прокси успешно проверен и работает.")
    try:
        session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
        bot = Bot(token=BOT_TOKEN, session=session) # type: ignore
        bot_info = await bot.get_me()
        print(f"\n🚀 Бот @{bot_info.username} успешно авторизован и готов к работе!")
        dp = Dispatcher()
        ai_service = AIService()
        db_service = db_module.DatabaseService()
        await db_service.init_db()  
        dp.include_router(router)
        await dp.start_polling(bot, ai_service=ai_service, db_service=db_service)
    except ValueError as e: 
        print(f"❌ Ошибка валидации токена: {e}")        
    except TelegramUnauthorizedError:  
        print("❌ Ошибка! Токен недействителен (401 Unauthorized) " \
        "Проверьте токен в @BotFather")  
    except Exception as e:
        print(f"❌ Произошла ошибка при запуске: {e}")


if __name__ == "__main__":
    asyncio.run(main())
