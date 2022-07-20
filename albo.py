import sys
import traceback
import requests
from bs4 import BeautifulSoup

from utils.formatting import get_formatted_department_tags, get_formatted_message
from utils.resources import *
from utils.tg import TelegramBot

ALBO_UNICT_URL = "http://albo.unict.it/"

tg_bot = TelegramBot.from_settings_file("settings.yaml")

def main ():    
    last_id = get_last_id("data/last_id.txt")

    cached_announcements = get_cached_announcements("data/cached_announcements.txt")

    page = requests.get(ALBO_UNICT_URL)

    if page.status_code != 200:
        print("Impossibile accedere al sito, riprovare più tardi")
        quit(1)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('div', id='boge')

    top_row = table.find('tr').find_next_sibling()

    if top_row is None:
        print("Nessun annuncio disponibile")
        return

    new_id = int(top_row.td.string)

    headers = [header.string for header in table.find('tr').find_all("td")]

    ids_to_parse = cached_announcements + list(range(last_id + 1, new_id + 1))

    #avoid channel flooding in case of error
    if len(ids_to_parse) > 10 and '--force-unsafe' not in sys.argv:
        ids_to_parse = []
        print("Troppi annunci da parsare, usare --force-unsafe per forzare l'invio")

    for id in ids_to_parse:
        td = table.find('td', text=id)

        if td is None:
            tg_bot.send_debug_messages("ID non trovato: " + str(id) + "\n" + "Probabilmente lo hanno saltato")
            if id in cached_announcements:
                cached_announcements.remove(id)
            continue

        tr = td.parent
        row = tr.find_all('td')

        message = get_formatted_message(row, headers)
        tags = get_formatted_department_tags(message)
        message = tags + "\n\n" + message
        
        try:
            attachments = [ALBO_UNICT_URL + list_item['href'] for list_item in tr.find_all('a')]
            cached_announcements = update_cached_announcements(cached_announcements, id, len(attachments))

            if len(attachments) != 0:
                tg_bot.send_telegram_announcements(attachments, message)

        except ValueError as err:
            cached_announcements = update_cached_announcements(cached_announcements, id, len(attachments))
            tg_bot.send_documents_error_message(err, id)

    write_new_id("data/last_id.txt", new_id)
    write_cached_announcements("data/cached_announcements.txt", cached_announcements)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_string = "An exception was raised:\n" + "`" + traceback.format_exc() +  "`"
        tg_bot.send_debug_messages(error_string)
        raise