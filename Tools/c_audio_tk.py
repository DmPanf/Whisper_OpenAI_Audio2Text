# python c_audio_tk.py
# Код для конвертации аудиофайлов с помощью tkinter и pydub

import os
from pydub import AudioSegment
from tkinter import Tk, filedialog

def convert_audio(input_file, output_format):
    """
    Конвертирует аудиофайл в указанный формат с помощью pydub.

    :param input_file: Путь к входному аудиофайлу
    :param output_format: Формат для конвертации (mp3, wav, aac, flac, ogg)
    """
    try:
        # Загружаем аудиофайл с использованием pydub
        audio = AudioSegment.from_file(input_file)

        # Получаем имя файла без расширения
        file_name, _ = os.path.splitext(input_file)

        # Определяем имя выходного файла
        output_file = f"{file_name}.{output_format}"

        # Экспортируем файл в новый формат
        audio.export(output_file, format=output_format)
        print(f"Файл {input_file} успешно конвертирован в {output_file}.")
    
    except Exception as e:
        print(f"Ошибка при конвертации {input_file}: {e}")

def choose_file_and_convert():
    """
    Открывает окно для выбора файла и конвертирует его в выбранный формат.
    """
    # Открываем окно для выбора файла
    Tk().withdraw()  # Скрыть основное окно Tkinter
    input_file = filedialog.askopenfilename(title="Выберите аудиофайл")

    if not input_file:
        print("Файл не выбран.")
        return

    # Запрашиваем формат для конвертации
    output_format = input("Введите формат для конвертации (mp3, wav, aac, flac, ogg): ").strip().lower()

    # Проверяем, поддерживается ли формат
    supported_formats = ["mp3", "wav", "aac", "flac", "ogg"]
    if output_format not in supported_formats:
        print(f"Неподдерживаемый формат: {output_format}. Поддерживаемые форматы: {', '.join(supported_formats)}")
        return

    # Конвертируем аудиофайл
    convert_audio(input_file, output_format)

if __name__ == "__main__":
    choose_file_and_convert()
