import json
import os
from pathlib import Path

from flask import current_app

from common.common_constants import MINECRAFT_SERVER_PATH


def read_user_stats(user_id):
    with open(os.path.join(current_app.config[MINECRAFT_SERVER_PATH], 'world', 'stats', f"{str(user_id)}.json"), 'r') as f:
        return json.load(f)

def get_user_ids_from_stats():
    dirent = Path(current_app.config[MINECRAFT_SERVER_PATH], 'world', 'stats')
    return [f.name.replace(".json", "") for f in dirent.iterdir() if f.is_file()]

def load_log_file():
    with open(os.path.join(current_app.config[MINECRAFT_SERVER_PATH], 'logs', "latest.log"), 'r') as f:
        return f.readlines()