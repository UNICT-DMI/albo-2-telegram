import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlencode, quote_plus
import yaml
from yaml.loader import SafeLoader
from typing import List, Union
import json
import re
import os.path

with open('settings.yaml') as f:
  data = yaml.load(f, Loader=SafeLoader)
  TOKEN, CHATID, CHAT_ID_DEV_LIST = data.values()

def escape_char (text: str, char_to_escape: List[str] = ['_', '*', '[', '`']) -> str:
  for char in char_to_escape:
    text = text.replace(char, "\\" + char)
  return text

def send_https_request (URL: str) -> None:
  r = requests.get(url = URL)
  responseJSON = r.json()
  if responseJSON["ok"] == False:
    raise ValueError (json.dumps(responseJSON, indent=2), URL.split("&")[-1])


def send_telegram_message(text: str, chat_id: Union[int, str] = CHATID) -> None:
    params = {
        'chat_id': chat_id,
        'parse_mode': 'markdown',
        'text': text
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?&" + urlencode(params, quote_via=quote_plus)
    send_https_request (URL)

def send_single_telegram_attachment(pdf_link: str, chat_id: Union[int, str] = CHATID) -> None:
    params = {
        'chat_id': chat_id,
        'disable_notification': True,
        'document': pdf_link
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendDocument?&" + urlencode(params, quote_via=quote_plus)
    send_https_request (URL)

def send_multiple_telegram_attachments(pdf_links: List[str], chat_id: Union[int, str] = CHATID) -> None:
    input_media_documents = [ {   "type": "document",  "media": pdf_link   }  for pdf_link in pdf_links]
    params = {
        'chat_id': chat_id,
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

with open("last_id.txt", "r") as f_id:
    last_id = int(f_id.read())

if not os.path.exists("cached_announcements"):
    open("cached_announcements.txt", "w").close()

with open("cached_announcements.txt", "r") as f_cached:
    cached_announcements = [int(cached_id) for cached_id in f_cached.read().splitlines()]

page = requests.get("http://albo.unict.it")

if page.status_code != 200:
  print("Impossibile accedere al sito, riprovare più tardi")

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('div', id='boge')

new_id = int (table.find('tr').find_next_sibling().td.string)

headers = [header.string for header in table.find('tr').find_all("td")]

# Special Headers in which is preferable to put a break line character to separate section of tg message
break_line_headers = ["Oggetto", "Inizio pubblicazione"]

ids_to_parse = cached_announcements + list(range(last_id + 1, new_id + 1))

for id in ids_to_parse:
  tr = table.find('td', text=id).parent
  row = tr.find_all('td')
  message = ""
  for i, header in enumerate(headers):
    if header in break_line_headers:
      message += "\n"
    message += "*" + header + "*: " + escape_char(row[i].span.string) + "\n"
  try:
    attachments = ["http://albo.unict.it/" + list_item['href'] for list_item in tr.find_all('a')]
    if len(attachments) == 0:
      if id not in cached_announcements:
        cached_announcements.append(id)
    else:
      if id in cached_announcements:
        cached_announcements.remove(id)
      send_telegram_message(message)
      send_telegram_attachments(attachments)
  except ValueError as err:
    decoded_url = json.dumps(unquote(err.args[1]))
    document_list = re.findall(r"https?:.+?(?=\\|\")", decoded_url)
    error_string = "```response sent: " + err.args[0] + "\n```" + "related documents:\n" + escape_char('\n'.join(document_list))
    print (json.dumps(unquote(err.args[1]))) #Insert here bot sending error message in group
    for dev in CHAT_ID_DEV_LIST:
      send_telegram_message(error_string, dev)
  #print(message)

with open("last_id.txt", "w+") as f_id:
    f_id.write(str(new_id))

with open("cached_announcements.txt", "w+") as f_cached:    
  for cached_id in cached_announcements:
      f_cached.write(str(cached_id) +  "\n")
