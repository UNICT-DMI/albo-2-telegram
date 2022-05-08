from datetime import date, datetime
import traceback
import requests
from bs4 import BeautifulSoup
import os.path
from utils.formatting import escape_char
from datetime import datetime

from utils.tg import Telegram_Bot

tg_bot = Telegram_Bot.from_settings_file("settings.yaml")

def main ():
  with open("data/last_id.txt", "r") as f_id:
      last_id = int(f_id.read())

  if not os.path.exists("data/cached_announcements"):
      open("data/cached_announcements.txt", "w").close()

  with open("data/cached_announcements.txt", "r") as f_cached:
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
      tg_bot.send_telegram_announcements(attachments, message)
    except ValueError as err:
      tg_bot.send_documents_error_message(err)
    #print(message)

  # with open("data/last_id.txt", "w+") as f_id:
  #     f_id.write(str(new_id))

  with open("data/cached_announcements.txt", "w+") as f_cached:    
    for cached_id in cached_announcements:
        f_cached.write(str(cached_id) +  "\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_string = "An exception was raised:\n" + "`" + escape_char(traceback.format_exc()) +  "`"
        tg_bot.send_debug_messages(error_string)
        raise