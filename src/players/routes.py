from flask import Blueprint

from src.players.server_api import retrieve_players_online, retrieve_player_details
from src.common.username_id_mappings import user_name_id_mapping

players_bp = Blueprint('players', __name__)

@players_bp.route('/online', methods=['GET'])
def show_online_players():
    players_online = retrieve_players_online()
    players = players_online['players']
    for player in players:
        online_player_details = retrieve_player_details(player['name'])
        player['details'] = online_player_details
    return players_online

@players_bp.route('/players', methods=['GET'])
def show_all_players():
    return user_name_id_mapping