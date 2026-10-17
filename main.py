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
from gigachat.exceptions import BadRequestError


logging.basicConfig(level=logging.INFO, 
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", 
            handlers=[logging.StreamHandler(sys.stdout), 
            logging.FileHandler("bot.log", encoding="utf-8")] )


logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")

if not BOT_TOKEN:
    logger.critical("Ошибка: Токен бота не найден! Проверьте файл .env")
    sys.exit()

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
            logger.critical(f"❌ Ошибка: Не валидный PROXY ({PROXY_URL}) просрочен или недоступен!")
            sys.exit()
        logger.info("✅ Прокси проверен, работает.")
    try:
        session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
        bot = Bot(token=BOT_TOKEN, session=session) # type: ignore
        bot_info = await bot.get_me()
        logger.info(f"\n🚀 Бот @{bot_info.username} авторизован, готов к работе!")
        dp = Dispatcher()
        ai_service = AIService()
        await ai_service.check_auth()
        db_service = db_module.DatabaseService()
        await db_service.init_db()  
        dp.include_router(router)
        await dp.start_polling(bot, ai_service=ai_service, db_service=db_service)
    except BadRequestError as e:
        logger.exception(f"❌ Ошибка авторизации GigaChat API: Неверный GIGACHAT_CREDENTIALS! {e}")
    except ValueError as e: 
        logger.exception(f"❌ Ошибка валидации токена: {e}")       
    except TelegramUnauthorizedError as e: 
        logger.exception(f"❌ Ошибка! Токен недействителен (401 Unauthorized) {e}") 
    except Exception as e:
        logger.exception(f"❌ Произошла ошибка при запуске: {e}")


if __name__ == "__main__":
    asyncio.run(main())
