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

def get_headers(table):
  headers = []
  for header in table.find('tr').find_all("td"):
    headers.append(header.string)
  return headers

f = open("last_id.txt", "r")
last_id = int(f.read())
f.close()

page = requests.get("http://albo.unict.it")

if page.status_code != 200:
  print("Impossibile accedere al sito, riprovare più tardi")

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('div', id='boge')

new_id = int (table.find('tr').find_next_sibling().td.string)

#print(new_id)

headers = get_headers(table)

for id in range (last_id + 1, new_id + 1):
  tr = table.find('td', text=id).parent
  row = tr.find_all('td')
  message = ""
  for i, header in enumerate(headers):
    #print(row[i].get_text())
    message = message + "*" + header + "*: " + row[i].span.string + "\n"
  send_telegram_message(message)
  print(message)

f = open("last_id.txt", "w+")
f.write(str(new_id))
f.close()
