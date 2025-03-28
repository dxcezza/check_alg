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
        
        # Получаем настройки прокси из переменных окружения
        http_proxy = 'http://127.0.0.1:8080'
        https_proxy = 'http://127.0.0.1:8080'
        
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
            return {"status": "success", "message": "Track downloaded successfully.", "output": output}
        else:
            logging.error(f"Процесс завершился с кодом ошибки: {process.returncode}")
            return {"status": "error", "message": f"Process exited with code {process.returncode}"}
    
    except FileNotFoundError:
        logging.error("Ошибка: spotdl не найден. Убедитесь, что он установлен.")
        return {"status": "error", "message": "spotdl not found."}
    except Exception as e:
        logging.error(f"Произошла непредвиденная ошибка: {e}")
        return {"status": "error", "message": str(e)}

@app.route('/download', methods=['POST'])
def download():
    # Получаем URL из JSON-запроса
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        logging.warning("URL не был передан в запросе.")
        return jsonify({"status": "error", "message": "URL is required."}), 400
    
    logging.info(f"Получен запрос на скачивание трека с URL: {url}")
    
    # Запускаем процесс скачивания
    result = download_track(url)
    
    # Возвращаем результат клиенту
    return jsonify(result)

if __name__ == "__main__":
    logging.info("Запуск бэкенда...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
