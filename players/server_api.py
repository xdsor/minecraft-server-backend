import re

from flask import current_app
from rcon.source.client import Client

from common.common_constants import SERVER_HOST, RCON_PASSWORD
from players.models.PlayerDetails import PlayerDetails
from players.models.PlayerList import PlayerList


def retrieve_players_online():
    with Client(current_app.config[SERVER_HOST], 25575, passwd=current_app.config[RCON_PASSWORD]) as client:
        response = client.run('list', 'uuids')
        return PlayerList(response).to_dict()

def retrieve_player_details(name):
    with Client(current_app.config[SERVER_HOST], 25575, passwd=current_app.config[RCON_PASSWORD]) as client:
        food_level_response = client.run(f'data get entity {name} foodLevel')
        health_response = client.run(f'data get entity {name} Health')
        experience_response = client.run(f'data get entity {name} XpLevel')
        food_level = _parse_entity_data(food_level_response)
        health = _parse_entity_data(health_response)
        experience = _parse_entity_data(experience_response)
        return PlayerDetails(food_level=food_level, health=health, experience=experience).to_dict()

def _parse_entity_data(data: str):
    match = re.search(r"([-+]?\d*\.\d+f?|[-+]?\d+)$", data)
    if match:
        num = match.group()
        return float(num[:-1]) if num.endswith('f') else int(num)
    else:
        raise ValueError("No numeric data found at the end of the input string.")
