import requests
import time
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("keep_alive.log"),
        logging.StreamHandler()
    ]
)

# URL вашего веб-приложения на Render
# Замените на URL вашего приложения после деплоя
APP_URL = "https://your-app-name.onrender.com/"

# Интервал пинга в секундах (каждые 10 минут)
PING_INTERVAL = 10 * 60

def ping_app():
    """Отправляет запрос на веб-приложение для поддержания его активности"""
    try:
        response = requests.get(APP_URL, timeout=10)
        if response.status_code == 200:
            logging.info(f"Пинг успешен: {response.status_code}")
            return True
        else:
            logging.warning(f"Пинг вернул код: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Ошибка при пинге: {e}")
        return False

def main():
    """Основная функция для периодического пинга"""
    logging.info("Запуск скрипта поддержания активности...")
    
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Отправка пинга в {now}")
        
        success = ping_app()
        
        if success:
            logging.info(f"Следующий пинг через {PING_INTERVAL} секунд")
        else:
            logging.warning(f"Пинг не удался, повторная попытка через {PING_INTERVAL} секунд")
        
        # Пауза перед следующим пингом
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main() 