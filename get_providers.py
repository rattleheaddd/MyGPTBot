import telebot

def get_provider_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    providers = sorted([
        "AllenAI", "ARTA", "Blackbox", "ChatGLM", "ChatGpt", "ChatGptEs", "Cloudflare", "Copilot", "DDG",
        "DeepInfraChat", "Dynaspark", "Free2GPT", "FreeGpt", "GizAI", "Glider", "Goabror", "ImageLabs",
        "Jmuz", "LambdaChat", "Liaobots", "OIVSCode", "PerplexityLabs", "Pi", "Pizzagpt", "PollinationsAI",
        "PollinationsImage", "TeachAnything", "TypeGPT", "You", "Websim", "Yqcloud",
    ])
    for provider in providers:
        markup.add(telebot.types.KeyboardButton(provider))
    return markup