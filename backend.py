from flask import Flask, request, jsonify
import subprocess
import logging
import os

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

def download_track(url):
    try:
        logging.info(f"Начинаем скачивание трека по URL: {url}")
        
        # Проверка корректности URL
        if not url.startswith("https://open.spotify.com/"):
            logging.error("Некорректный URL.")
            return {"status": "error", "message": "Invalid URL."}
        
        # Получаем настройки прокси из переменных окружения
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        
        if not http_proxy or not https_proxy:
            logging.warning("Прокси не настроен. Используется прямое соединение.")
        
        # Формируем команду spotdl с учетом прокси
        proxy_args = f"--proxy {http_proxy}" if http_proxy else ""
        command = f"spotdl {url} {proxy_args}"
        logging.debug(f"Выполняем команду: {command}")
        
        # Устанавливаем временную директорию для скачивания файлов
        download_dir = os.getenv("DOWNLOAD_DIR", "/tmp/downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        # Запускаем процесс с перехватом stdout и stderr
        env = os.environ.copy()
        if http_proxy:
            env["HTTP_PROXY"] = http_proxy
        if https_proxy:
            env["HTTPS_PROXY"] = https_proxy
        
        with subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env) as process:
            output = []
            
            # Выводим stdout в реальном времени
            for line in process.stdout:
                output.append(line.strip())
                logging.debug(f"STDOUT: {line.strip()}")
            
            # Проверяем stderr после завершения процесса
            stderr = process.stderr.read()
            if stderr:
                logging.error(f"STDERR: {stderr}")
                return {"status": "error", "message": stderr.strip()}
        
        # Проверяем код завершения процесса
        if process.returncode == 0:
            logging.info("Скачивание завершено успешно!")
