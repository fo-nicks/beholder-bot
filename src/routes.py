from logging         import out
from dice.exceptions import DiceBaseException
from dice            import roll
from telegram        import args_from

HELP = ('*Misc commands:*\n' +
       '/roll ndS - where _n_ is number of dice and _S_ is number of sides')

def roll_dice_command(message) :
    args = args_from(message)
    try: 
        result = roll(args[1])
        if isinstance(result, list):
            if len(result) > 1:
                rolls_as_str = [str(roll) for roll in result]
                output = '{} | {}'.format(', '.join(rolls_as_str), sum(result))
            else:
                output = str(result[0])
        else:
            output = str(result)
        return output
    except Exception as e:
        out(e)
        return 'Nope.'


