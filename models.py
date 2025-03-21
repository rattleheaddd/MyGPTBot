# models.py
import telebot

def get_model_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    models = sorted([
        'deepseek-chat', 'deepseek-v3', 'deepseek-r1', 'grok-3', 'grok-3-r1', 'gpt-4o', 'gpt-4o-mini',
        'o1', 'o1-mini', 'o3-mini', 'gpt-4', "GigaChat:latest", "meta-ai", "gemini-2.0", "gemini-exp",
        "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-thinking", "gemini-2.0-pro",
        "claude-3-haiku", "claude-3-sonnet", "claude-3-opus", "claude-3.5-sonnet", "claude-3.7-sonnet", "claude-3.7-sonnet-thinking"
    ])
    for model in models:
        markup.add(telebot.types.KeyboardButton(model))
    return markup
