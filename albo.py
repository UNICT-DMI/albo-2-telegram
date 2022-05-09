import traceback
import requests
from bs4 import BeautifulSoup

from utils.departments import find_all_departments
from utils.formatting import escape_char, get_formatted_message
from utils.resources import *
from utils.tg import TelegramBot

tg_bot = TelegramBot.from_settings_file("settings.yaml")

def main ():    
    last_id = get_last_id("data/last_id.txt")

    cached_announcements = get_cached_announcements("data/cached_announcements.txt")

    page = requests.get("http://albo.unict.it")

    if page.status_code != 200:
        print("Impossibile accedere al sito, riprovare più tardi")
        quit(1)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('div', id='boge')

    new_id = int(table.find('tr').find_next_sibling().td.string)

    headers = [header.string for header in table.find('tr').find_all("td")]

    ids_to_parse = cached_announcements + list(range(last_id + 1, new_id + 1))

    for id in ids_to_parse:
        tr = table.find('td', text=id).parent
        row = tr.find_all('td')

        message = get_formatted_message(row, headers)
        tags = ' '.join(["*[" + department + "]*" for department in find_all_departments(message)])
        message = tags + "\n\n" + message
        
        try:
            attachments = ["http://albo.unict.it/" + list_item['href'] for list_item in tr.find_all('a')]
            cached_announcements = update_cached_announcements(cached_announcements, id, len(attachments))

            if len(attachments) != 0:
                tg_bot.send_telegram_announcements(attachments, message)

        except ValueError as err:
            tg_bot.send_documents_error_message(err)

    write_new_id("data/last_id.txt", new_id)
    write_cached_announcements("data/cached_announcements.txt", cached_announcements)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_string = "An exception was raised:\n" + "`" + escape_char(traceback.format_exc()) +  "`"
        tg_bot.send_debug_messages(error_string)
        raise