# python c_wav-to-mp3.py

from pydub import AudioSegment
import os

def convert_wav_to_mp3(wav_file, output_mp3_file):
    """
    Конвертирует аудиофайл из формата WAV в MP3 с использованием библиотеки pydub.

    :param wav_file: Путь к файлу WAV, который нужно конвертировать
    :param output_mp3_file: Путь к выходному файлу MP3
    """
    try:
        # Загружаем аудиофайл
        audio = AudioSegment.from_wav(wav_file)
        
        # Конвертация в MP3
        audio.export(output_mp3_file, format="mp3")
        print(f"Файл {wav_file} успешно конвертирован в {output_mp3_file}.")
    
    except Exception as e:
        print(f"Ошибка при конвертации {wav_file} в MP3: {e}")

# Пример использования:
wav_file = "./audio/audio_10.wav"
output_mp3_file = "./audio/audio_10.mp3"

# Выполняем конвертацию
convert_wav_to_mp3(wav_file, output_mp3_file)
