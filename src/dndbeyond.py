from http.client import HTTPSConnection
from telegram    import args_from
from logging     import out

import json
import os

DNDBEYOND_URL = 'www.dndbeyond.com'
CONNECTION = HTTPSConnection(DNDBEYOND_URL)
CACHE_PATH = '/cache/dndbeyond-cache.json'

SET_CHARACTER_HELP = '/setcharacter <name> <id> - track a D&D Beyond character'
STATS_HELP = '/stats <name> - get character stats'
HELP = '*D&D Beyond commands*\n{}\n{}'.format(
    SET_CHARACTER_HELP, 
    STATS_HELP
)

def update_cache(cache) :
    cache_file = open(CACHE_PATH, 'w+')
    cache_file.write(json.dumps(cache))

def init_cache() :
    if not os.path.isfile(CACHE_PATH):
        cache = CACHE_SCHEMA
        update_cache(cache)
    else:
        cache_file = open(CACHE_PATH, 'r')
        cache = json.load(cache_file)
    return cache

CACHE_SCHEMA = {
    'characters': {}
}
CACHE = init_cache()

def dndbeyond_json_from(character_id) :
    CONNECTION.request('GET', '/character/{}/json'.format(character_id))
    json_bytes = CONNECTION.getresponse().read()
    json_str   = str(json_bytes, 'utf-8')
    return json.loads(json_str)

def character_id_from(name):
    try:
        character_id = CACHE['characters'][name]
    except KeyError as e:
        out(e)
        character_id = None
    return character_id

def set_character_command(message) :
    args = args_from(message)
    try:
        name = args[1]
        character_id = args[2]
        CACHE['characters'][name] = character_id
        update_cache(CACHE)
        return '{} added with ID {}'.format(name, character_id)
    except IndexError as e:
        out(e)
        return ('Incorrect number of arguments. \n' +
                'Expected usage: "/setcharacter <character_name> <character_id>"')

def pretty_stats(stats):
    stat_dict = { stat['id']: stat['value'] for stat in stats }
    stre = stat_dict[1]
    dex  = stat_dict[2]
    con  = stat_dict[3]
    inte = stat_dict[4]
    wis  = stat_dict[5]
    cha  = stat_dict[6]
    pretty = '\nSTR: {}\nDEX: {}\nCON: {}\nINT: {}\nWIS: {}\nCHA: {}\n'.format(
        stre,
        dex,
        con,
        inte,
        wis,
        cha
    )
    return pretty

def stats_command(message) :
    args = args_from(message)
    try:
        name = args[1]
        character_id = character_id_from(name)
        if character_id != None:
            character_json = dndbeyond_json_from(character_id)
            stats = character_json['stats']
            stats = pretty_stats(stats)
            return stats
        else:
            return 'Could not find character with name: {}'.format(name)
    except Exception as e:
        out(e)
        return 'Error: problem with fetching or constructing character stats'
