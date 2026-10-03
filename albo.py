import sys
import traceback

import requests
from bs4 import BeautifulSoup

from utils.resources import *
from utils.tg import TelegramBot
lazy from utils.formatting import get_formatted_department_tags, get_formatted_message

ALBO_UNICT_URL = "http://albo.unict.it/"

tg_bot = TelegramBot.from_settings_file("settings.yaml")


def main():
    last_id = get_last_id("data/last_id.txt")

    cached_announcements = get_cached_announcements("data/cached_announcements.txt")

    page = requests.get(ALBO_UNICT_URL)

    if page.status_code != 200:
        print("Cannot reach the albo site, try again later")
        sys.exit(1)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("div", id="boge")
    if table is None:
        raise RuntimeError("div#boge not found on the albo page")

    header_row = table.find("tr")
    if header_row is None:
        raise RuntimeError("Header row not found in the albo table")

    top_row = header_row.find_next_sibling()

    if top_row is None:
        print("No announcements available")
        return

    id_cell = top_row.td
    if id_cell is None:
        raise RuntimeError("ID cell not found in the first albo row")

    new_id = int(id_cell.get_text())

    # Without data/last_id.txt start from the newest announcement, instead of posting the whole backlog
    if last_id is None:
        print("data/last_id.txt not found, starting from ID " + str(new_id))
        last_id = new_id

    headers = [header.get_text() for header in header_row.find_all("td")]

    ids_to_parse = cached_announcements + list(range(last_id + 1, new_id + 1))

    # avoid channel flooding in case of error
    if len(ids_to_parse) > 10 and "--force-unsafe" not in sys.argv:
        ids_to_parse = []
        print("Too many announcements to parse, use --force-unsafe to send them anyway")

    for id in ids_to_parse:
        td = table.find("td", string=str(id))

        if td is None:
            tg_bot.send_debug_messages(
                "ID not found: " + str(id) + "\n" + "It was probably skipped"
            )
            if id in cached_announcements:
                cached_announcements.remove(id)
            continue

        tr = td.parent
        if tr is None:
            raise RuntimeError("Row of announcement " + str(id) + " not found")

        row = tr.find_all("td")

        message = get_formatted_message(row, headers)
        tags = get_formatted_department_tags(message)
        message = tags + "\n\n" + message

        try:
            attachments = [
                ALBO_UNICT_URL + str(list_item["href"])
                for list_item in tr.find_all("a")
            ]
            cached_announcements = update_cached_announcements(
                cached_announcements, id, len(attachments)
            )

            if len(attachments) != 0:
                tg_bot.send_telegram_announcements(attachments, message)

        except ValueError as err:
            cached_announcements = update_cached_announcements(
                cached_announcements, id, len(attachments)
            )
            tg_bot.send_documents_error_message(err, id)

    write_new_id("data/last_id.txt", new_id)
    write_cached_announcements("data/cached_announcements.txt", cached_announcements)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        error_string = "An exception was raised:\n" + "`" + traceback.format_exc() + "`"
        tg_bot.send_debug_messages(error_string)
        raise
