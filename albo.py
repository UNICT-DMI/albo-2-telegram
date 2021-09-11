from selenium import webdriver
import requests
from urllib.parse import urlencode, quote_plus

TOKEN = ""
CHATID = 123456

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')

def send_telegram_message(text):
    params = {
        'chat_id': CHATID,
        'text': text
    }
    URL = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?&parse_mode=markdown&" + urlencode(params, quote_via=quote_plus)
    r = requests.get(url = URL)


headers = [
  "Numero",
  "Data registrazione",
  "Richiedente",
  "Oggetto",
  "Inizio pubblicazione",
  "Fine pubblicazione",
]

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://ws1.unict.it/albo/')

file = open('last_id.txt', 'r')
last_id = int(file.read())
file.close()

id = driver.execute_script("return document.querySelectorAll('.records tr')[1].querySelectorAll('td')[0].innerText")

if last_id != id:
  diff = int(id) - last_id

  for x in range(diff):
    data = driver.execute_script("return [...document.querySelectorAll('.records tr')[" + str(x+1) +"].querySelectorAll('td')].map(x => x.querySelector('span').innerText)")

    content = ""

    for idx in range(len(headers)):
      print(headers[idx] + ": " + data[idx])
      content += "*" + headers[idx] + "*: " + data[idx] + "\n"

    print("\n")
    send_telegram_message(content)

# update id
file = open("last_id.txt", "w+")
file.write(id)
file.close()
