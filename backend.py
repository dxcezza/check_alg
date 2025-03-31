import os

def download_track_from_spotify(track_url, output_directory="."):
    """
    Скачивает трек из Spotify с использованием spotdl.

    :param track_url: URL трека на Spotify.
    :param output_directory: Директория для сохранения трека.
    """
    # Проверяем, существует ли указанная директория
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Формируем команду для spotdl
    command = f"spotdl --bitrate disable {track_url} --output {output_directory}"

    # Выполняем команду в CLI
    print(f"Выполняется команда: {command}")
    result = os.system(command)

    # Проверяем результат выполнения команды
    if result == 0:
        print("Трек успешно скачан!")
    else:
        print("Произошла ошибка при скачивании трека.")

# Пример использования
if __name__ == "__main__":
    # URL трека на Spotify
    spotify_track_url = "https://open.spotify.com/track/5AMaSh2CGFCGC8wRGSQlJA"

    # Директория для сохранения трека
    output_dir = "./downloads"

    # Скачиваем трек
    download_track_from_spotify(spotify_track_url, output_dir)
