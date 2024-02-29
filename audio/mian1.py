# main1.py

import os
import whisper
import time

audio_path = '/content/drive/MyDrive/DATA/Audio'
text_path = '/content/drive/MyDrive/Whisper/Ogul.English'
model_name = 'large'

# Загрузка модели Whisper
model = whisper.load_model(model_name)

def transcribe_audio(model, audio_file):
    # Выполнение транскрибации
    result = model.transcribe(audio_file)
    return result['text']

# Перебор всех файлов в директории audio_path
for root, dirs, files in os.walk(audio_path):
    for file in files:
        if file.endswith(".m4a"):  # Проверка расширения файла
            audio_file = os.path.join(root, file)
            start_time = time.time()  # Начало измерения времени
            
            # Вызов функции транскрибации
            text = transcribe_audio(model, audio_file)
            
            end_time = time.time()  # Конец измерения времени
            my_time = round(end_time - start_time, 2)
            
            # Вывод информации о файле и времени обработки
            print(f"Обработка файла {file} заняла {my_time} секунд.")
            
            # Вывод последних трех строк текста
            last_lines = text.split('\n')[-3:]
            print("\n\n".join(last_lines))
            
            # Создание пути для сохранения текстового файла, включая подпапку для каждой части
            base_name = os.path.splitext(file)[0]  # Без расширения файла
            save_path = os.path.join(text_path, base_name)
            os.makedirs(save_path, exist_ok=True)  # Создание подпапки, если ее нет
            text_file_path = os.path.join(save_path, f"{base_name}.txt")
            
            # Сохранение текста в файл
            with open(text_file_path, 'w') as text_file:
                text_file.write(text)
