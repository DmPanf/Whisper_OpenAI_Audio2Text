# python c_mp3-to-wav.py

from pydub import AudioSegment

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1)  # Конвертация в моно
    audio = audio.set_frame_rate(16000)  # Установка частоты дискретизации 16000 Гц
    audio.export(output_file, format="wav")
    print(f"Файл {input_file} конвертирован в {output_file}.")

# Пример использования:
convert_to_wav("./audio/audio_02.mp3", "./audio/audio_02.wav")
