import json
import re
from typing import List, Union
from urllib.parse import quote_plus, unquote, urlencode
import requests
import yaml
from utils.formatting import escape_char

class TelegramBot:
    def __init__(self, token: str, chat_id: Union[int, str], dev_chat_ids: List[str]) -> None:
        self.token = token
        self.chat_id = chat_id
        self.dev_ids = dev_chat_ids
        pass

    @classmethod
    def from_settings_file (cls, filename: str) -> 'TelegramBot':
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            token, chat_id, dev_chat_ids = data.values()
        return cls(token, chat_id, dev_chat_ids)

    def send_https_request (self, URL: str) -> None:
        r = requests.get(url = URL)
        responseJSON = r.json()
        if responseJSON["ok"] == False:
            raise ValueError (json.dumps(responseJSON, indent=2), URL.split("&")[-1])

    def send_telegram_message(self, text: str, chat_id: Union[str, int] = None) -> None:
        if chat_id == None:
            chat_id = self.chat_id
        params = {
            'chat_id': chat_id,
            'parse_mode': 'markdown',
            'text': text
        }
        URL = "https://api.telegram.org/bot" + self.token + "/sendMessage?&" + urlencode(params, quote_via=quote_plus)
        self.send_https_request (URL)

    def send_single_telegram_attachment(self, pdf_link: str, caption: str = '') -> None:
        params = {
            'chat_id': self.chat_id,
            'caption': caption,
            'parse_mode': 'markdown',
            'disable_notification': caption == '',
            'document': pdf_link
        }
        URL = "https://api.telegram.org/bot" + self.token + "/sendDocument?&" + urlencode(params, quote_via=quote_plus)
        self.send_https_request (URL)

    def send_multiple_telegram_attachments(self, pdf_links: List[str]) -> None:
        input_media_documents = [ {   "type": "document",  "media": pdf_link   }  for pdf_link in pdf_links]
        params = {
            'chat_id': self.chat_id,
            'disable_notification': True,
            'media': json.dumps(input_media_documents),
        }
        URL = "https://api.telegram.org/bot" + self.token + "/sendMediaGroup?&" + urlencode(params, quote_via=quote_plus)
        self.send_https_request (URL)

    def send_telegram_announcements(self, pdf_links: List[str], message: str) -> None:
        if len(pdf_links) == 1:
            if len(message) < 1024: 
                self.send_single_telegram_attachment(pdf_links[0], message)
            else:
                self.send_single_telegram_attachment(pdf_links[0])
                self.send_telegram_message(message)
        else:
            self.send_multiple_telegram_attachments(pdf_links)
            self.send_telegram_message(message)
    
    def send_documents_error_message(self, err: ValueError, id: int) -> None:
        decoded_url = json.dumps(unquote(err.args[1]))
        document_list = re.findall(r"https?:.+?(?=\\|\")", decoded_url)
        error_string = "id:" + str(id) + "\n" + "``` response sent: " + err.args[0] + "\n```" + "related documents:\n" + escape_char('\n'.join(document_list))
        print (json.dumps(unquote(err.args[1])))
        self.send_debug_messages(error_string)

    def send_debug_messages(self, message: str) -> None:
        for dev in self.dev_ids:
            self.send_telegram_message(message, dev)
