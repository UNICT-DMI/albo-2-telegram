import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus

TOKEN = ""
CHATID = 123456

def send_telegram_message(text: str) -> None:
    params = {
        'chat_id': CHATID,
        'text': text
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?&parse_mode=markdown&" + urlencode(params, quote_via=quote_plus)
    r = requests.get(url = URL)

with open("last_id.txt", "r") as f:
    last_id = int(f.read())

page = requests.get("http://albo.unict.it")

if page.status_code != 200:
  print("Impossibile accedere al sito, riprovare più tardi")

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('div', id='boge')

new_id = int (table.find('tr').find_next_sibling().td.string)

headers = headers = [header.string for header in table.find('tr').find_all("td")]

# Special Headers in which is preferable to put a break line character to separate section of tg message
break_line_headers = ["Oggetto", "Inizio pubblicazione"]

for id in range (last_id + 1, new_id + 1):
  tr = table.find('td', text=id).parent
  row = tr.find_all('td')
  message = ""
  for i, header in enumerate(headers):
    if header in break_line_headers:
      message+="\n"
    message = message + "*" + header + "*: " + row[i].span.string.replace("*", "\\*").replace("_", "\\_") + "\n"
  send_telegram_message(message)
  print(message)

with open("last_id.txt", "w+") as f:
    f.write(str(new_id))
