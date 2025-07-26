import logging
import asyncio
from aiogram import Bot, Dispatcher
import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_local.log"),
        logging.StreamHandler()
    ]
)

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)

async def main():
    # Импортируем диспетчер из основного файла бота
    from bot import dp
    
    # Удаляем вебхук перед запуском поллинга
    await bot.delete_webhook()
    logging.info("Вебхук удален")
    
    # Запускаем поллинг
    logging.info("Запуск бота в режиме поллинга")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.info("Запуск бота")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
    except Exception as e:
        logging.exception(f"Ошибка при запуске бота: {e}") 