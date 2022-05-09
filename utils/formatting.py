from typing import List

# Special Headers in which is preferable to put a break line character to separate section of tg message
break_line_headers = ["Oggetto", "Inizio pubblicazione"]

def escape_char (text: str, char_to_escape: List[str] = ['_', '*', '[', '`']) -> str:
    for char in char_to_escape:
        text = text.replace(char, "\\" + char)
    return text

def get_formatted_message(row, headers: List[str]) -> str:
    message = ""
    for i, header in enumerate(headers):
        if header in break_line_headers:
            message += "\n"          
        message += "*" + header + "*: " + escape_char(row[i].span.string) + "\n"
    return message
