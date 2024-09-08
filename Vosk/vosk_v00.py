# python vosk_v00.py
# https://github.com/alphacep/vosk-api/tree/master/training

import os
import pyaudio
import json
import threading
import keyboard
from vosk import Model, KaldiRecognizer
from queue import Queue

# Путь к модели
MODEL_PATH = "./model/vosk-model-small-ru-0.22"  # меньшая модель для быстрой загрузки

# Флаг для остановки программы
stop_event = threading.Event()

# Функция для загрузки модели и начала распознавания
def load_and_recognize():
    global stop_event

    # Проверяем наличие модели
    if not os.path.exists(MODEL_PATH):
        print(f"Модель не найдена по пути {MODEL_PATH}")
        stop_event.set()
        return

    # Загрузка модели
    print("Загрузка модели...")
    model = Model(MODEL_PATH)
    print("Модель загружена.")

    # Инициализация микрофона
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    # Инициализация распознавателя
    rec = KaldiRecognizer(model, 16000)

    print("🎙 Начало записи. Говорите что-нибудь...")

    try:
        while not stop_event.is_set():
            # Захват аудиоданных с микрофона
            data = stream.read(4000, exception_on_overflow=False)

            # Если данные достаточно длинные, запускаем распознавание
            if rec.AcceptWaveform(data):
                result = rec.Result()
                text = json.loads(result).get("text", "")
                print(f"Распознано: {text}")
            else:
                partial_result = rec.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "")
                if partial_text:
                    print(f"Частичное распознавание: {partial_text}")

    except KeyboardInterrupt:
        pass

    finally:
        # Остановка потока
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("🛑 Остановка записи.")

# Функция для отслеживания нажатия ESC
def check_for_esc():
    global stop_event
    while not stop_event.is_set():
        if keyboard.is_pressed('esc'):
            print("⏹ Завершение по ESC")
            stop_event.set()

# Основная функция
def main():
    # Запускаем потоки
    recognition_thread = threading.Thread(target=load_and_recognize)
    esc_thread = threading.Thread(target=check_for_esc)

    recognition_thread.start()
    esc_thread.start()

    # Ожидание завершения работы потоков
    recognition_thread.join()
    esc_thread.join()

    print("Программа завершена.")

if __name__ == "__main__":
    main()
