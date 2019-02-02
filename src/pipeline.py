from logging  import out
from telegram import reply
import sys

def command_name_from(message):
    try:
        text = message['text']
        command = text.split(',')[0]
        if command.startswith('/'):
            command = command[1:].split(' ')[0]
    except (KeyError, IndexError) :
        command = None
    return command
        
class CommandRouter:
    def __init__(self):
        self.commands = {}

    def add_route(self, name, handler) :
        self.commands[name] = handler

    def route(self, message):
        command_name = command_name_from(message)
        try:
            response = self.commands[command_name](message)
            reply(message, response)
        except KeyError:
            pass

