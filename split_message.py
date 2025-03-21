def split_message(text, max_length=4000):
    """Разбивает текст на части, чтобы избежать ошибки Telegram (4096 символов)"""
    parts = []
    while text:
        parts.append(text[:max_length])
        text = text[max_length:]
    return parts