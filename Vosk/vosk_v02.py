# python vosk_v02.py
# https://github.com/alphacep/vosk-api/tree/master/python

import os
import pyaudio
import json
import time
import keyboard
import threading
from vosk import Model, KaldiRecognizer

# Путь к модели
# MODEL_PATH = "./model/vosk-model-ru-0.42"   # Тяжелая большая модель
MODEL_PATH = "./model/vosk-model-small-ru-0.22" # Маленькая легкая модель

# Проверяем, доступна ли модель
if not os.path.exists(MODEL_PATH):
    print(f"🚫 Модель не найдена по пути {MODEL_PATH}")
    exit(1)

# Загружаем модель
print("...Загрузка модели...")
model = Model(MODEL_PATH)
print("✅ Модель загружена.")

# Инициализация микрофона
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Инициализация распознавателя
rec = KaldiRecognizer(model, 16000)

def check_for_esc(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed('esc'):
            print("⏹ Завершение по ESC")
            stop_event.set()

# Функция для вывода с временными метками
def print_with_timestamp(text, start_time):
    elapsed_time = time.time() - start_time
    print(f"[{elapsed_time:.2f}s] {text}")

def main():
    print("🎙  Начало записи...")

    stop_event = threading.Event()
    start_time = time.time()

    # Запуск потока для остановки по ESC
    esc_thread = threading.Thread(target=check_for_esc, args=(stop_event,))
    esc_thread.start()

    buffer_duration = 8  # Длительность блока в секундах
    buffer_start_time = time.time()  # Время начала блока
    collected_text = []  # Накопленный текст за 8 секунд

    try:
        while not stop_event.is_set():
            # Захват аудиоданных с микрофона
            data = stream.read(4000, exception_on_overflow=False)

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
                    print_with_timestamp(f"🔰 {full_text}", buffer_start_time)
                    collected_text = []  # Очищаем накопленный текст
                buffer_start_time = time.time()  # Обновляем время начала блока

    except KeyboardInterrupt:
        print("🛑 Остановка записи.")
    
    finally:
        # Останавливаем поток
        stream.stop_stream()
        stream.close()
        p.terminate()
        stop_event.set()
        esc_thread.join()

if __name__ == "__main__":
    main()
