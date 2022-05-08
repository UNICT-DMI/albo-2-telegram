from typing import List

def escape_char (text: str, char_to_escape: List[str] = ['_', '*', '[', '`']) -> str:
  for char in char_to_escape:
    text = text.replace(char, "\\" + char)
  return text
