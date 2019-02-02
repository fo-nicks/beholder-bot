from logging         import out
from dice.exceptions import DiceBaseException
from dice            import roll

def _args_from(message):
    try:
        text = message['text']
        args = text.split(' ')
    except KeyError:
        args = []
    return args

def roll_dice_command(message) :
    args = _args_from(message)
    try: 
        return roll(args[1])
    except (IndexError, DiceBaseException):
        return 'Nope.'


