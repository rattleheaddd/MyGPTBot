from g4f.Provider import FreeGpt
from g4f.client import Client

def analyze_with_chatgpt(message, chat_history, model, provider):
    client = Client()

    # Формируем историю сообщений для отправки в GPT
    messages = chat_history + [{"role": "user", "content": message}]

    # Ограничиваем количество сообщений
    if len(messages) > 10:
        messages = messages[-10:]

    try:
        response = client.chat.completions.create(
            model=model,
            provider=provider,
            messages=messages,
            web_search=False
        )
        # Получаем ответ
        response_text = response.choices[0].message.content

        # Убираем LaTeX (символы $$ и экранирование)
        response_text = response_text.replace('$$', '')
        response_text = response_text.replace('\\', '')

        # Форматируем математические выражения для Telegram
        response_text = response_text.replace('r^2', 'r²')
        response_text = response_text.replace('sqrt', '√')

        # Заменяем математические формулы на текстовый вид
        response_text = response_text.replace('[', '').replace(']', '')

        return response_text

    except Exception as err:
        print(f"Ошибка с моделью {model}: {err}")
        return None
