import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import gradio as gr

home = "C:\\Users\\bunta\\Documents\\ARCHIVE\\Python.Projects\\Whisper"
# os.getcwd() 
# C:\Users\bunta\AppData\Local\Temp\gradio\a8d6d311c86e1dd7713ade12d71b1ce95e57552e\На острове свободы.txt

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
    result = pipe(audio_path)["text"]  # , language='en'
    
    # Сохранение результата в файл с тем же именем, но с расширением .txt
    # t_path = os.path.splitext(audio_path)[0] + ".txt"
    t_path = os.path.basename(os.path.splitext(audio_path)[0]) + ".txt"
    text_path = os.path.join(home, 'audio', t_path)
    print(f'\n🔰text_path')
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    return result

# Настройте интерфейс Gradio
interface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(type="filepath"),
    outputs=gr.Textbox(),
    title="Speech to Text Transcription",
    description="Upload an audio file and get the transcription." #,
    #max_content_length=100 * 1024 * 1024  # Увеличьте размер контента до 100MB
)

# Запустите приложение
if __name__ == "__main__":
    interface.launch()
