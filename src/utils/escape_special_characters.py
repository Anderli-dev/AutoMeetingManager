import re


def escape_special_characters(input_string):
    # Визначаємо спеціальні символи
    special_chars = re.escape(r'`~!@#$%^&*()-_=+[{]}\\|;:\'\",<.>/?')
    # Шукаємо спеціальні символи та додаємо перед ними "\\"
    escaped_string = re.sub(f"([{special_chars}])", r"\\\1", input_string)
    return escaped_string
