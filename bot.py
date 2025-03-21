import telebot
from config import TOKEN
from models import get_model_keyboard
from pdf_handler import extract_text_from_pdf
from gpt_handler import analyze_with_chatgpt
from split_message import split_message
from utils import save_file_to_disk, remove_file
from format_text import format_text

bot = telebot.TeleBot(TOKEN)

user_models = {}
user_histories = {}

VALID_MODELS = {
    'deepseek-chat', 'deepseek-v3', 'deepseek-r1', 'grok-3', 'grok-3-r1', 'gpt-4o', 'gpt-4o-mini',
    'o1', 'o1-mini', 'o3-mini', 'gpt-4', "GigaChat:latest", "meta-ai", "gemini-2.0", "gemini-exp",
    "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-thinking", "gemini-2.0-pro",
    "claude-3-haiku", "claude-3-sonnet", "claude-3-opus", "claude-3.5-sonnet", "claude-3.7-sonnet", "claude-3.7-sonnet-thinking"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Задавай мне вопросы или отправляй PDF/txt файлы для анализа.\nВведи /help, чтобы узнать, какие у меня есть команды.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Доступные команды на данный момент:\n" + "/models - выбрать модель, которая будет использоваться для ответа.\n" + "/start - начать сессию.")

@bot.message_handler(commands=['models'])
def send_models(message):
    bot.send_message(message.chat.id, "Выберите модель:", reply_markup=get_model_keyboard())

@bot.message_handler(func=lambda message: message.text in VALID_MODELS)
def handle_model_selection(message):
    user_models[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Вы выбрали модель: {message.text}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id not in user_histories:
        user_histories[user_id] = []

    user_message = message.text
    user_histories[user_id].append({"role": "user", "content": user_message})

    selected_model = user_models.get(user_id, 'gpt-4o')
    response = analyze_with_chatgpt(user_message, user_histories[user_id], selected_model)

    if response is None:
        bot.send_message(message.chat.id, "Извините, выбранная модель недоступна. Пожалуйста, выберите другую модель.", reply_markup=get_model_keyboard())
    else:
        response = format_text(response)
        user_histories[user_id] = user_histories[user_id][-100:]

        for part in split_message(response):
            bot.send_message(message.chat.id, part, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    if message.document.mime_type in ('application/pdf', 'text/plain') or message.document.file_name.endswith(('.pdf', '.txt')):
        bot.send_message(message.chat.id, "Получен файл. Я начинаю его анализировать. Пожалуйста, подождите...")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_path = f"temp_{message.document.file_name}"
        save_file_to_disk(file_path, downloaded_file)

        try:
            if message.document.mime_type == 'application/pdf':
                text_for_analysis = extract_text_from_pdf(file_path)
            else:
                with open(file_path, "r", encoding="utf-8") as file:
                    text_for_analysis = file.read()

            if not text_for_analysis.strip():
                raise ValueError("Не удалось извлечь текст из файла. Попробуйте другой файл.")

            user_id = message.chat.id
            if user_id not in user_histories:
                user_histories[user_id] = []

            user_histories[user_id].append({"role": "user", "content": text_for_analysis})

            selected_model = user_models.get(user_id, 'gpt-4o')
            analysis = analyze_with_chatgpt("Сделай полный анализ текста:\n" + text_for_analysis, user_histories[user_id], selected_model)

            if analysis is None:
                bot.send_message(message.chat.id, "Извините, выбранная модель недоступна. Пожалуйста, выберите другую модель.", reply_markup=get_model_keyboard())
            else:
                analysis = format_text(analysis)
                for part in split_message(analysis):
                    bot.send_message(message.chat.id, f"📄 Анализ вашего файла:\n\n{part}", parse_mode="HTML")
                user_histories[user_id] = user_histories[user_id][-100:]

        except ValueError as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
        except Exception as err:
            bot.send_message(message.chat.id, f"Произошла ошибка при обработке файла: {str(err)}")
        finally:
            remove_file(file_path)

bot.polling(none_stop=True)
