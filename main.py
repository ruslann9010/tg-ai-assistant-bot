import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv  # Импортируем библиотеку для чтения .env

# Включаем логирование, чтобы видеть запуск бота в терминале
logging.basicConfig(level=logging.INFO)

# Загружаем переменные из файла .env в окружение
load_dotenv()

# Безопасно достаем токен
API_TOKEN = os.getenv("BOT_TOKEN")

# Проверка на случай, если вы забыли создать файл или опечатались в имени переменной
if not API_TOKEN:
    sys.exit("Ошибка: Токен бота не найден! Проверьте файл .env")

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def main():
    # Наше информационное сообщение
    print("\n🚀 Бот успешно запущен и готов к работе!")
    # Запуск прослушивания серверов Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())