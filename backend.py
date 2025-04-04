import requests

def send_download_request(video_url):
    # URL вашего локального сервера (через Tuna)
    local_server_url = "https://aestci-85-198-105-37.ru.tuna.am/download"

    # Отправляем POST-запрос на локальный сервер
    payload = {"url": video_url}
    response = requests.post(local_server_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        print(result["message"])
    else:
        print(f"Ошибка: {response.text}")

# Пример использования
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=uQj99W1Ul9U"
    send_download_request(youtube_url)
