import os
import requests
import sys

# Замените на ваш токен API PythonAnywhere
API_TOKEN = "YOUR_API_TOKEN"
USERNAME = "YOUR_USERNAME"

# Базовый URL для API
API_BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

def upload_file(local_path, remote_path):
    """Загружает файл на PythonAnywhere"""
    with open(local_path, 'rb') as f:
        content = f.read()
    
    response = requests.post(
        f"{API_BASE_URL}/files/path{remote_path}",
        headers={"Authorization": f"Token {API_TOKEN}"},
        data=content
    )
    
    if response.status_code == 201:
        print(f"Файл {local_path} успешно загружен в {remote_path}")
        return True
    else:
        print(f"Ошибка при загрузке файла {local_path}: {response.text}")
        return False

def create_directory(path):
    """Создает директорию на PythonAnywhere"""
    response = requests.post(
        f"{API_BASE_URL}/files/path{path}",
        headers={"Authorization": f"Token {API_TOKEN}"},
        json={"operation": "mkdir"}
    )
    
    if response.status_code == 201:
        print(f"Директория {path} успешно создана")
        return True
    else:
        print(f"Ошибка при создании директории {path}: {response.text}")
        return False

def upload_project():
    """Загружает все файлы проекта на PythonAnywhere"""
    # Создаем директорию для проекта
    create_directory("/telegrambot")
    
    # Список файлов для загрузки
    files_to_upload = [
        "bot.py",
        "config.py",
        "custom_methods.py",
        "gpt_answer.py",
        "requirements.txt",
        "run_bot.py"
    ]
    
    # Создаем директорию для медиафайлов
    create_directory("/telegrambot/media")
    
    # Добавляем медиафайлы
    for i in range(1, 5):
        files_to_upload.append(f"media/{i}.jpg")
    
    # Загружаем файлы
    for file in files_to_upload:
        if os.path.exists(file):
            remote_path = f"/telegrambot/{file}"
            upload_file(file, remote_path)
        else:
            print(f"Файл {file} не найден")

if __name__ == "__main__":
    print("Начало загрузки файлов на PythonAnywhere...")
    upload_project()
    print("Загрузка завершена!") 