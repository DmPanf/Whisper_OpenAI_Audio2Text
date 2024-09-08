# python vosk_v01.py
# https://github.com/alphacep/vosk-api/tree/master/python

import os
import wave
import json
import time
from vosk import Model, KaldiRecognizer

# Путь к модели
# MODEL_PATH = "./model/vosk-model-ru-0.42"   # Тяжелая большая модель
MODEL_PATH = "./model/vosk-model-small-ru-0.22" # Маленькая легкая модель

# Проверяем, доступна ли модель
if not os.path.exists(MODEL_PATH):
    print(f"Модель не найдена по пути {MODEL_PATH}")
    exit(1)

# Загружаем модель
print("Загрузка модели...")
model = Model(MODEL_PATH)
print("Модель загружена.")

# Функция для вывода с временными метками
def print_with_timestamp(text, start_time):
    elapsed_time = time.time() - start_time
    print(f"[{elapsed_time:.2f}s] {text}")

# Функция для обработки аудиофайла
def process_audio_file(file_path, model, buffer_duration=8):
    # Открываем аудиофайл
    wf = wave.open(file_path, "rb")

    # Проверяем формат аудио
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("Аудиофайл должен быть моно, 16-битный и с частотой 16000 Гц.")
        exit(1)

    # Инициализация распознавателя
    rec = KaldiRecognizer(model, wf.getframerate())

    buffer_start_time = time.time()  # Время начала обработки
    collected_text = []  # Накопленный текст за 8 секунд

    print(f"🎙 Обработка файла: {file_path}")

    # Чтение данных по частям
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        # Если данные достаточно длинные, запускаем распознавание
        if rec.AcceptWaveform(data):
            # Выводим полный распознанный текст с временной меткой
            result = rec.Result()
            text = json.loads(result).get("text", "")
            if text:
                collected_text.append(text)

        # Проверяем, прошло ли 8 секунд для вывода блока
        if time.time() - buffer_start_time >= buffer_duration:
            if collected_text:
                # Выводим накопленный текст за блок 8 секунд
                full_text = " ".join(collected_text)
                print_with_timestamp(f"Блок текста: {full_text}", buffer_start_time)
                collected_text = []  # Очищаем накопленный текст
            buffer_start_time = time.time()  # Обновляем время начала блока

    # Выводим остатки текста, если что-то осталось
    if collected_text:
        full_text = " ".join(collected_text)
        print_with_timestamp(f"Блок текста: {full_text}", buffer_start_time)

    wf.close()
    print(f"🛑 Обработка файла завершена: {file_path}")

# Основная функция для обработки файлов
def main():
    # Пример обработки нескольких файлов
    audio_files = ["./audio/audio_01.wav", "./audio/audio_02.wav"]  # Список аудио файлов

    for file_path in audio_files:
        process_audio_file(file_path, model)

if __name__ == "__main__":
    main()
