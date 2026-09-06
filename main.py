import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv  # Импортируем библиотеку для чтения .env
from handlers import router
from aiogram.client.session.aiohttp import AiohttpSession 

# Включаем логирование, чтобы видеть запуск бота в терминале
logging.basicConfig(level=logging.INFO)

# Загружаем переменные из файла .env в окружение
load_dotenv()

# Безопасно достаем токен
API_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")

# Проверка на случай, если вы забыли создать файл или опечатались в имени переменной
if not API_TOKEN:
    sys.exit("Ошибка: Токен бота не найден! Проверьте файл .env")

 
async def main():

    session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
    # Инициализируем бота и диспетчер
    bot = Bot(token=API_TOKEN, session=session) # type: ignore
    dp = Dispatcher()

    # Наше информационное сообщение
    print("\n🚀 Бот успешно запущен и готов к работе!")
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())