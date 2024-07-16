# !pip install -q openai==0.28.1
#

import openai
import getpass
import os
import time

# Получение ключа API от пользователя и установка его как переменной окружения
openai_key = getpass.getpass("OpenAI API Key:")
os.environ["OPENAI_API_KEY"] = openai_key
openai.api_key = openai_key

promt = "Ты работаешь в качестве AI-генератора текста, специализирующегося на создании реалистичных отзывов. Твоя задача - создавать убедительные и детализированные негативные отзывы на автомобили Tesla, основываясь на часто упоминаемых недостатках таких автомобилей, как проблемы с аккумуляторной батареей, качество сборки, навигация, программное обеспечение и обслуживание клиентов. Отзывы должны быть оригинальными, содержать разнообразные мнения и выражать различные аспекты пользовательского опыта, включая дизайн, удобство использования, технические характеристики, стоимость обслуживания и общее удовлетворение автомобилем."
zapros = "Cгенерируй 50 уникальных и детализированных негативных отзывов о Tesla, охватывающих разнообразные проблемы и мнения пользователей. Каждый отзыв должен быть выразителен и предоставлять конкретные детали или личные впечатления, которые могут включать технические недостатки, личные разочарования или недовольство аспектами автомобиля."

messages = [
      {"role": "system", "content": promt},
      {"role": "user", "content": zapros}
      ]
# Загрузка исходного датасета
df = pd.read_csv('./updated_reviews.csv')

# Количество необходимых негативных отзывов
new_num = 1550

while df[df['label'] == 0].shape[0] < new_num:
    # Генерация 40 негативных отзывов
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=3000
    )
    generated_reviews = response['choices'][0]['message']['content'].strip().split('\n')[:-1]

    # Добавление сгенерированных отзывов в датасет
    new_reviews_df = pd.DataFrame({'review': generated_reviews, 'label': [0] * len(generated_reviews)})
    df = pd.concat([df, new_reviews_df], ignore_index=True)

    # Пауза на 20 секунд
    time.sleep(20)

# Сохранение финального датасета
df.to_csv('./final_reviews.csv', index=False)

# Вывод информации о финальном датасете
print("\nКоличество негативных отзывов:", df[df['label'] == 0].shape[0])
print("\nПять случайных негативных отзывов:")
print(df[df['label'] == 0].sample(5)['review'])

# Визуализация распределения отзывов
plt.figure(figsize=(8, 6))
sns.countplot(x='label', data=df)
plt.title('Распределение позитивных и негативных отзывов')
plt.xlabel('Класс отзыва')
plt.ylabel('Количество')
plt.xticks([0, 1], ['Негативные', 'Позитивные'])
plt.show()
