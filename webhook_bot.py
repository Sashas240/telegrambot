import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import config
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("webhook_bot.log"),
        logging.StreamHandler()
    ]
)

# Инициализация бота и диспетчера
TOKEN = config.BOT_TOKEN
WEBHOOK_HOST = 'https://xvcen.pythonanywhere.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Импортируем обработчики из основного файла бота
try:
    from bot import dp as main_dp
    dp.include_router(main_dp)
    logging.info("Обработчики из основного бота успешно импортированы")
except Exception as e:
    logging.error(f"Ошибка импорта обработчиков: {e}", exc_info=True)

# Обработчик для проверки работы вебхука
@dp.message(commands=["ping"])
async def ping_command(message: types.Message):
    await message.answer("Pong! Webhook работает!")

async def on_startup():
    # Устанавливаем вебхук при запуске
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Вебхук установлен: {WEBHOOK_URL}")

async def on_shutdown():
    # Удаляем вебхук при остановке
    await bot.delete_webhook()
    logging.info("Вебхук удален")

# Создаем приложение aiohttp
app = web.Application()

# Настраиваем вебхук
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)
webhook_handler.register(app, path=WEBHOOK_PATH)

# Устанавливаем обработчики запуска и завершения
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Запускаем приложение (для локального тестирования)
if __name__ == "__main__":
    logging.info("Запуск вебхук-сервера")
    web.run_app(app, host="localhost", port=8000)