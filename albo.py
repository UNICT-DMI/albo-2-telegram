import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus
from typing import List
import json

TOKEN = ""
CHATID = 123456

def escape_char (text: str, char_to_escape: List[str] = ['_', '*', '[', '`']) -> str:
  for char in char_to_escape:
    text = text.replace(char, "\\" + char)
  return text

def send_https_request (URL: str) -> None:
  r = requests.get(url = URL)
  responseJSON = r.json()
  if responseJSON["ok"] == False:
    raise ValueError (json.dumps(responseJSON, indent=2), URL.split("&")[-1])


def send_telegram_message(text: str, chat_id = CHATID) -> None:
    params = {
        'chat_id': chat_id,
        'parse_mode': 'markdown',
        'text': text
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?&" + urlencode(params, quote_via=quote_plus)
    send_https_request (URL)

def send_single_telegram_attachment(pdf_link: str) -> None:
    params = {
        'chat_id': CHATID,
        'disable_notification': True,
        'document': pdf_link
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendDocument?&" + urlencode(params, quote_via=quote_plus)
    send_https_request (URL)

def send_multiple_telegram_attachments(pdf_links: List[str]) -> None:
    input_media_documents = [ {   "type": "document",  "media": pdf_link   }  for pdf_link in pdf_links]
    params = {
        'chat_id': CHATID,
        'disable_notification': True,
        'media': json.dumps(input_media_documents),
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendMediaGroup?&" + urlencode(params, quote_via=quote_plus)
    send_https_request (URL)

def send_telegram_attachments(pdf_links: List[str]) -> None:
    if len(pdf_links) == 1:
      send_single_telegram_attachment(pdf_links[0])
    else:
      send_multiple_telegram_attachments(pdf_links)

with open("last_id.txt", "r") as f:
    last_id = int(f.read())

page = requests.get("http://albo.unict.it")

if page.status_code != 200:
  print("Impossibile accedere al sito, riprovare più tardi")

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('div', id='boge')

new_id = int (table.find('tr').find_next_sibling().td.string)

headers = [header.string for header in table.find('tr').find_all("td")]

# Special Headers in which is preferable to put a break line character to separate section of tg message
break_line_headers = ["Oggetto", "Inizio pubblicazione"]

for id in range (last_id + 1, new_id + 1):
  tr = table.find('td', text=id).parent
  row = tr.find_all('td')
  message = ""
  for i, header in enumerate(headers):
    if header in break_line_headers:
      message += "\n"
    message += "*" + header + "*: " + escape_char(row[i].span.string) + "\n"
  try:
    send_telegram_message(message)
    attachments = ["http://albo.unict.it/" + list_item['href'] for list_item in tr.find_all('a')]
    send_telegram_attachments(attachments)
  except ValueError as err:
    error_string = "response sent: " + err.args[0] + "\n" + "last parameter: "+ err.args[1]
    print (error_string) #Insert here bot sending error message in group
  #print(message)

with open("last_id.txt", "w+") as f:
    f.write(str(new_id))
