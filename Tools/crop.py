# python crop.py

from pydub import AudioSegment

# Загрузка исходного аудиофайла
audio = AudioSegment.from_mp3("./audio/LCA_Test 2-Part 4.mp3")

# Время в миллисекундах
start_time = 1 * 60 * 1000 + 16 * 1000  # 0:01:16 (в миллисекундах)
end_time = 5 * 60 * 1000 + 12 * 1000    # 0:05:12 (в миллисекундах)

# Обрезка аудио
cropped_audio = audio[start_time:end_time]

# Сохранение обрезанного аудио в новый файл
cropped_audio.export("./audio/audio_00e.mp3", format="mp3")

print("Обрезка завершена, файл сохранён как audio_00e.mp3.")
