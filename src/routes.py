from logging         import out
from dice.exceptions import DiceBaseException
from dice            import roll
from telegram        import args_from

HELP = ('*Misc commands:*\n' +
       '/roll ndS    - where _n_ is number of dice and _S_ is number of sides\n' +
       '/dc   ncD    - where _n_ is number of dice and _C_ is DC to beat\n' +
       '      n|mcD  - same as above, but will add modifier _m_ to each roll')

def _dc_values_from(message):
    args = args_from(message)
    args = ''.join(args[1:]).split('c')
    out('ARGS:' + str(args))
    try:
        dice_and_mod = args[0]
        n_dice = dice_and_mod
        dc = args[1]
    except KeyError:
        return None

    # Determine if modifier argument is present
    mod = ''
    try:
        dice_and_mod = dice_and_mod.split('|')
        if len(dice_and_mod) > 1:
            mod = dice_and_mod[1]
            n_dice = dice_and_mod[0]
    except KeyError:
        pass

    out('DICE N: ' + str(n_dice))
    out('MODIFIER:' + mod)
    out('DC: ' + str(dc))

    # Cast to integer values
    n_dice = int(n_dice)
    dc = int(dc)
    if mod != '': mod = int(mod)
    else:        mod = 0

    return (n_dice, mod, dc)

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

def dc_dice_command(message) :
    try: 
        n_dice, mod, dc = _dc_values_from(message)
        command = '(({}d20).+{})'.format(n_dice, mod)
        result = roll(command)
        saves = 0
        fails = 0
        if isinstance(result, list):
            for dice_roll in result:
                dice_roll = int(dice_roll)
                if dice_roll + mod >= dc: 
                    saves += 1
                    out('SAVE: d{}+{} vs {}'.format(dice_roll, mod, dc))
                else:
                    out('FAIL: d{}+{} vs {}'.format(dice_roll, mod, dc))
                    fails += 1
        output  = '*DC {}* Saving Throw \n' 
        if mod > 0: 
            output += '+{} modifier added to each roll\n'.format(mod) 
        output += 'Saves: {}\n'
        output += 'Fails: {}\n'
        output = output.format(dc, saves, fails)
        return output
    except Exception as e:
        out(e)
        return 'Nope.'

