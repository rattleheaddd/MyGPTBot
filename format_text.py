import re

def format_text(text):
    """Форматирует текст: **жирный** → <b>жирный</b>"""
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)