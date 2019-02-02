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
        result = roll(args[1])
        if len(result) > 1:
            rolls_as_str = [str(roll) for roll in result]
            output = '{} | {}'.format(', '.join(rolls_as_str), sum(result))
        else:
            output = str(result[0])
        return output
    except Exception as e:
        out(e)
        return 'Nope.'


