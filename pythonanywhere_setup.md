# Настройка Always-on задачи на PythonAnywhere

## Шаги для настройки Always-on задачи (для платных аккаунтов)

1. Перейдите на вкладку "Tasks" в панели управления PythonAnywhere
2. В разделе "Always-on tasks" нажмите "Add a new always-on task"
3. Введите команду для запуска бота:
   ```
   cd ~/telegrambot && ~/.virtualenvs/mybot/bin/python3 run_bot.py
   ```
4. Нажмите "Create" для создания задачи

## Настройка Web-worker (для бесплатных аккаунтов)

Если у вас бесплатный аккаунт, вы можете настроить Web-worker:

1. Перейдите на вкладку "Web" в панели управления
2. Нажмите "Add a new web app"
3. Выберите "Manual configuration" и Python 3.9
4. Укажите путь к виртуальному окружению: `/home/YOUR_USERNAME/.virtualenvs/mybot`
5. Отредактируйте файл WSGI:

```python
import os
import sys

# Добавьте путь к вашему проекту
path = '/home/YOUR_USERNAME/telegrambot'
if path not in sys.path:
    sys.path.append(path)

# Запустите бота в отдельном потоке
import threading
import time

def run_bot():
    import asyncio
    from bot import bot, dp
    
    # Небольшая задержка перед запуском
    time.sleep(5)
    
    # Запускаем бота
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dp.start_polling(bot))

# Запускаем бота в отдельном потоке
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

# Стандартное приложение Flask для PythonAnywhere
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Bot is running"]
```

6. Нажмите "Reload" для перезапуска веб-приложения

## Проверка работы бота

После настройки проверьте логи на наличие ошибок:
```
tail -f ~/telegrambot/bot.log
```

## Дополнительные рекомендации

1. Регулярно проверяйте логи бота
2. Настройте автоматическое перезапуск бота в случае сбоя
3. Используйте try-except блоки для обработки ошибок в коде бота 