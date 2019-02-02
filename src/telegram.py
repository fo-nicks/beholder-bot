from http.client  import HTTPSConnection
from logging      import out 
from urllib.parse import urlencode

import sys
import time
import json
import os

TELEGRAM_URL = 'api.telegram.org'
TOKEN = 'bot' + os.environ['TELEGRAM_TOKEN']
CONNECTION = HTTPSConnection(TELEGRAM_URL)
POLLING_INTERVAL = 1

# Fetch raw data from Telegram API endpoint
def get(endpoint):
    CONNECTION.request('GET', '/{}/{}'.format(TOKEN, endpoint))
    return CONNECTION.getresponse().read()

def post(endpoint, params):
    headers = {"Content-type": "application/x-www-form-urlencoded",            "Accept": "text/plain"} 
    encoded_params = urlencode(params)
    CONNECTION.request(
        'POST', '/{}/{}'.format(TOKEN, endpoint), 
        encoded_params,
        headers
    )
    CONNECTION.getresponse().read()

def reply(message, response):
    try:
        chat_id = message['chat']['id']
        user = message['from']
        if 'username' in user: name = user['username']
        else                 : name = user['first_name']
        to = '@' + name
        full_response = '{} {}'.format(to, response)
        endpoint = 'sendMessage'
        params = {'chat_id':chat_id, 'text':full_response}
        post(endpoint, params)
    except KeyError:
        pass

def messages_after(offset):
    bytea = get(
        'getUpdates?offset={}&timeout={}'
            .format(
                str(offset),
                str(POLLING_INTERVAL)
            )
    )
    try:
        updates = json.loads(bytea)['result']
        last_update_id = updates[len(updates) - 1]['update_id']
        messages = (
            last_update_id,
            [update['message'] for update in updates]
        )
    except (KeyError, IndexError):
        messages = (offset, [])
    return messages

