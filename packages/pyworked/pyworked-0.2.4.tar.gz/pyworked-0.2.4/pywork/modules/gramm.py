import time
import json
import requests

class Gramm:

    def __init__(self, token, method):
        self.string = "https://api.telegram.org/bot" + token + "/" + method

    def get_bot_id(self):
        res = requests.post(self.string).json()
        return(res['result']['id'])

    def get_is_bot(self):
        res = requests.post(self.string).json()
        return(res['result']['is_bot'])
    
    def get_bot_first_name(self):
        res = requests.post(self.string).json()
        return(res['result']['first_name'])

    def get_bot_username(self):
        res = requests.post(self.string).json()
        return(res['result']['username'])

    def get_bot_can_join_groups(self):
        res = requests.post(self.string).json()
        return(res['result']['can_join_groups'])

    def get_bot_can_read_all_group_messages(self):
        res = requests.post(self.string).json()
        return(res['result']['can_read_all_group_messages'])
    
    def get_bot_supports_inline_queries(self):
        res = requests.post(self.string).json()
        return(res['result']['supports_inline_queries'])

    def send_message(self, chat_id, text):
        res = requests.post(self.string,
            params={
                'chat_id': chat_id,
                'text': text
            }
        ).json()
        res = {
            'message_id': res['result']['message_id'],
            'bot_id': res['result']['from']['id'],
            'is_bot': res['result']['from']['is_bot'],
            'bot_first_name': res['result']['from']['first_name'],
            'bot_username': res['result']['from']['username'],
            'chat_id': res['result']['chat']['id'],
            'to_first_name': res['result']['chat']['first_name'],
            'to_username': res['result']['chat']['username'],
            'text': res['result']['text']
        }
        return(res)

