# python gpu.py
# Вывод имени вашей видеокарты

import torch
print(torch.cuda.is_available())  # Должно вернуть True
print(torch.cuda.get_device_name(0))  # Вывод имени вашей видеокарты

#import tensorflow as tf
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
