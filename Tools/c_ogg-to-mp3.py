# python c_ogg-to-mp3.py

from pydub import AudioSegment

# Загружаем .ogg файл
audio = AudioSegment.from_file("./audio/audio_03.ogg", format="ogg")

# Конвертируем и сохраняем в .mp3
audio.export("./audio/audio_03.mp3", format="mp3")
# audio.export("output.mp3", format="mp3", bitrate="192k")
