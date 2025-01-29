import re


def escape_special_characters(input_string):
    # Define special characters
    special_chars = re.escape(r'`~!@#$%^&*()-_=+[{]}\\|;:\'\",<.>/?')
    # Look for special characters and add before them "\"
    escaped_string = re.sub(f"([{special_chars}])", r"\\\1", input_string)
    return escaped_string
