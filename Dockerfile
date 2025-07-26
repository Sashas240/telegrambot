FROM python:3.9-slim

WORKDIR /app

# Установка необходимых пакетов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn aiohttp

# Копирование файлов проекта
COPY . .

# Создание директории для логов
RUN mkdir -p /app/logs

# Открытие порта
EXPOSE 10000

# Запуск приложения
CMD ["gunicorn", "render_bot:app", "--bind", "0.0.0.0:10000", "--worker-class", "aiohttp.GunicornWebWorker"] 