from logging import out
from telegram import messages_after
from pipeline import CommandRouter

import dndbeyond
import routes

def help_command(messages): 
    response = (
       '\n' + dndbeyond.HELP + '\n\n' +
       routes.HELP
    )

    return response

COMMAND_ROUTER = CommandRouter()
COMMAND_ROUTER.add_route('help', help_command)
COMMAND_ROUTER.add_route('roll', routes.roll_dice_command)
COMMAND_ROUTER.add_route('setcharacter', dndbeyond.set_character_command)
COMMAND_ROUTER.add_route('stats', dndbeyond.stats_command)


def process_messages(messages):
    for message in messages:
        out('\n-> ' + message['text'])
        COMMAND_ROUTER.route(message)

def event_loop():
    latest_update_id = 0
    while True:
        update_id, messages = messages_after(latest_update_id + 1)
        process_messages(messages)
        message_count = len(messages)
        if   message_count == 0: 
            latest_update_id = 0
        else:
            latest_update_id = update_id

out("beholder-bot startup complete. Listening for incoming messages...")
event_loop()
