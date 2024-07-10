# python app_v2.py
# pip install pydub
# 1.Разделение аудио на минутные сегменты
# 2.Обработка каждого сегмента
# 3.Вывод сообщения о прогрессе
# 4.Сохранение результата в файл

import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import gradio as gr

home = "C:\\Users\\${USER}\\Documents\\${PROJECTS}\\Python.Projects\\Whisper"

# Определите устройство (GPU или CPU)
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Загрузите модель и процессор
model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Создайте pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device,
)

# Определите функцию транскрибирования
def transcribe(audio_path):
    audio = AudioSegment.from_file(audio_path)
    chunks = make_chunks(audio, 60 * 1000)  # Разделение на минутные сегменты

    result = ""
    for i, chunk in enumerate(chunks):
        chunk_path = f"{audio_path}_chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_result = pipe(chunk_path)["text"]
        result += chunk_result + " "
        print(f"Processed {i + 1} minute(s) of audio")

    # Сохранение результата в файл с тем же именем, но с расширением .txt
    t_path = os.path.basename(os.path.splitext(audio_path)[0]) + ".txt"
    text_path = os.path.join(home, 'audio', t_path)
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result.strip())
    
    return result.strip()

# Настройте интерфейс Gradio
interface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(type="filepath"),
    outputs=gr.Textbox(),
    title="Speech to Text Transcription",
    description="Upload an audio file and get the transcription."
)

# Запустите приложение
if __name__ == "__main__":
    interface.launch()
