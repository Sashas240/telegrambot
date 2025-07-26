import requests
import sys
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Импорт токена из конфига
try:
    import config
    TOKEN = config.BOT_TOKEN
except ImportError:
    # Если не удалось импортировать, пробуем получить из переменных окружения
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        logging.error("Не удалось получить токен бота. Укажите его в аргументах или в config.py")
        sys.exit(1)

def set_webhook(webhook_url=None):
    """Устанавливает вебхук для бота"""
    # Если URL не указан, пытаемся получить из аргументов или переменных окружения
    if not webhook_url:
        if len(sys.argv) > 1:
            webhook_url = sys.argv[1]
        else:
            webhook_url = os.environ.get('RENDER_EXTERNAL_URL')
            if webhook_url:
                webhook_url = f"{webhook_url}/webhook"
            else:
                logging.error("URL вебхука не указан. Укажите его в аргументах или в переменной окружения RENDER_EXTERNAL_URL")
                sys.exit(1)
    
    # Формируем URL для установки вебхука
    api_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    
    # Отправляем запрос
    try:
        response = requests.post(api_url, json={"url": webhook_url})
        result = response.json()
        
        if result.get("ok"):
            logging.info(f"Вебхук успешно установлен на {webhook_url}")
            logging.info(f"Ответ API: {result}")
            return True
        else:
            logging.error(f"Ошибка при установке вебхука: {result}")
            return False
    except Exception as e:
        logging.error(f"Исключение при установке вебхука: {e}")
        return False

def get_webhook_info():
    """Получает информацию о текущем вебхуке"""
    api_url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(api_url)
        result = response.json()
        
        if result.get("ok"):
            logging.info("Информация о вебхуке:")
            logging.info(result["result"])
            return result["result"]
        else:
            logging.error(f"Ошибка при получении информации о вебхуке: {result}")
            return None
    except Exception as e:
        logging.error(f"Исключение при получении информации о вебхуке: {e}")
        return None

if __name__ == "__main__":
    # Если указан аргумент --info, получаем информацию о вебхуке
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        get_webhook_info()
    # Если указан аргумент --delete, удаляем вебхук
    elif len(sys.argv) > 1 and sys.argv[1] == "--delete":
        api_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        try:
            response = requests.post(api_url)
            result = response.json()
            if result.get("ok"):
                logging.info("Вебхук успешно удален")
            else:
                logging.error(f"Ошибка при удалении вебхука: {result}")
        except Exception as e:
            logging.error(f"Исключение при удалении вебхука: {e}")
    # Иначе устанавливаем вебхук
    else:
        webhook_url = None
        if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
            webhook_url = sys.argv[1]
        
        set_webhook(webhook_url)
        # Проверяем, что вебхук установлен
        get_webhook_info()