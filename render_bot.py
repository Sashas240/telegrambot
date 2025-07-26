import logging
import asyncio
from aiogram import types, Dispatcher, Bot, F
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import config
import os
import json
from bot import handle_business_connect, start_command, handle_gifts_list, handle_gift_callback
from bot import handle_transfer, show_star_users, show_user_star_balance, transfer_stars_to_admin
from bot import convert_menu, convert_select_handler, convert_exec_handler, test
from bot import select_chat_handler, select_group_handler, liquid_nft_handler, my_gifts_handler
from bot import analyze_chat_callback, start_liquidity_analysis, show_top_liquid, show_illiquid
from bot import detailed_gift_analysis, evaluate_gifts, handle_verify, check_auth_handler
from bot import transfer_gift_handler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Инициализация бота и диспетчера
TOKEN = config.BOT_TOKEN
WEBHOOK_HOST = os.environ.get('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
dp.business_connection()(handle_business_connect)
dp.message(F.text == "/start")(start_command)
dp.message(F.text == "/gifts")(handle_gifts_list)
dp.callback_query(F.data.startswith("gifts:"))(handle_gift_callback)
dp.callback_query(F.data.startswith("transfer:"))(handle_transfer)
dp.message(F.text == "/stars")(show_star_users)
dp.callback_query(F.data.startswith("stars:"))(show_user_star_balance)
dp.callback_query(F.data.startswith("transfer_stars:"))(transfer_stars_to_admin)
dp.message(F.text == "/convert")(convert_menu)
dp.callback_query(F.data.startswith("convert_select:"))(convert_select_handler)
dp.callback_query(F.data.startswith("convert_exec:"))(convert_exec_handler)
dp.message(F.text == "/test")(test)
dp.message(F.text == "/select_chat")(select_chat_handler)
dp.message(F.text == "/select_group")(select_group_handler)
dp.message(F.text == "/liquid_nft")(liquid_nft_handler)
dp.message(F.text == "/my_gifts")(my_gifts_handler)
dp.callback_query(F.data.startswith("analyze_chat:"))(analyze_chat_callback)
dp.callback_query(F.data == "start_liquidity_analysis")(start_liquidity_analysis)
dp.callback_query(F.data == "show_top_liquid")(show_top_liquid)
dp.callback_query(F.data == "show_illiquid")(show_illiquid)
dp.callback_query(F.data == "detailed_gift_analysis")(detailed_gift_analysis)
dp.callback_query(F.data == "evaluate_gifts")(evaluate_gifts)
dp.callback_query(F.data == "verify")(handle_verify)
dp.callback_query(F.data == "check_auth")(check_auth_handler)
dp.message(F.text.startswith("/transfer"))(transfer_gift_handler)

# Обработчик для проверки работы вебхука
@dp.message(F.text == "/ping")
async def ping_command(message: types.Message):
    await message.answer("Pong! Webhook работает!")

async def on_startup(app):
    # Устанавливаем вебхук
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Установлен вебхук: {WEBHOOK_URL}")
    logging.info(f"Бот @{(await bot.me()).username} запущен")

async def on_shutdown(app):
    # Удаляем вебхук
    await bot.delete_webhook()
    logging.info("Вебхук удален")

def create_app():
    # Создаем приложение aiohttp
    app = web.Application()
    
    # Настраиваем вебхук
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)
    
    # Добавляем обработчики для главной страницы
    async def handle_root(request):
        return web.Response(text="Bot is running")
    
    app.router.add_get('/', handle_root)
    
    # Устанавливаем обработчики запуска и завершения
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    return app

# Для запуска на Render
app = create_app()

# Для локального запуска
if __name__ == "__main__":
    logging.info("Запуск вебхук-сервера")
    PORT = int(os.environ.get('PORT', 8000))
    web.run_app(app, host='0.0.0.0', port=PORT) 