from flask import current_app
from rcon.source import Client

from src.common.common_constants import SERVER_HOST, RCON_PASSWORD
from src.common.utils.fsutils import read_user_stats, read_user_advancements
from src.players.server_api import retrieve_players_online
from src.common.username_id_mappings import user_name_id_mapping


def _extract_advancements_count(advancements):
    result = 0
    for key, value in advancements.items():
        if not isinstance(value, dict):
            continue
        if value["done"]:
            advancement_type = key.split(":")[1].split("/")[0]
            if advancement_type in ["story", "nether", "end", "adventure", "husbandry"]:
                result += 1
    return result


def get_all_stats():
    players_online_response = retrieve_players_online().get('players')
    players_online = players_online_response if players_online_response else []
    players_online_names = list(map(lambda x: x['name'], players_online))

    result = []
    for name, uuid in user_name_id_mapping.items():
        online = name in players_online_names
        try:
            stats = read_user_stats(uuid)["stats"]
            stats_custom = stats.get("minecraft:custom")
            stats_mined = stats.get("minecraft:mined")
            stats_crafted = stats.get("minecraft:crafted")
            stats_killed = stats.get("minecraft:killed")

            play_time = stats_custom.get("minecraft:play_time") if stats_custom else 0
            blocks_mined = sum(stats_mined.values()) if stats_mined else 0
            items_crafted = sum(stats_crafted.values()) if stats_crafted else 0
            mob_killed = sum(stats_killed.values()) if stats_killed else 0
            time_since_death = stats_custom.get("minecraft:time_since_death") if stats_custom else 0
            time_since_rest = stats_custom.get("minecraft:time_since_rest") if stats_custom else 0

            advancements = read_user_advancements(uuid)
            advancements_count = _extract_advancements_count(advancements)

            result.append({
                "online": online,
                "name": name,
                "play_time": play_time,
                "blocks_mined": blocks_mined,
                "items_crafted": items_crafted,
                "mob_killed": mob_killed,
                "time_since_death": time_since_death,
                "time_since_rest": time_since_rest,
                "advancements_count": advancements_count
            })
        except FileNotFoundError as e:
            current_app.logger.error(e)
            continue
    return result

def get_server_time():
    with Client(current_app.config[SERVER_HOST], 25575, passwd=current_app.config[RCON_PASSWORD]) as client:
        day_response = client.run("time query day")
        game_time_response = client.run("time query gametime")
        daytime_response = client.run("time query daytime")

        day = _parse_time(day_response)
        game_time = _parse_time(game_time_response)
        daytime = _parse_time(daytime_response)

        return {'day': day, 'game_time': game_time, 'daytime': daytime}

def _parse_time(response):
    return int(response.split("The time is ")[1])