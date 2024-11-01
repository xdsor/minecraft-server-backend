import re
from typing import Dict, List


class PlayerList:
    def __init__(self, message: str):
        self.online_count = 0
        self.max_players = 0
        self.players: List[Dict[str, str]] = []
        self._parse_message(message)

    def _parse_message(self, message: str):
        match = re.match(r"There are (\d+) of a max of (\d+) players online:?(.*)", message)
        if match:
            self.online_count = int(match.group(1))
            self.max_players = int(match.group(2))

            players_str = match.group(3).strip()
            if players_str:
                player_matches = re.findall(r"(\w+) \(([\w-]+)\)", players_str)
                self.players = [{"name": name, "id": uuid} for name, uuid in player_matches]

    def to_dict(self):
        return {
            "online_count": self.online_count,
            "max_players": self.max_players,
            "players": self.players
        }

    def __repr__(self):
        return (f"PlayerList(online_count={self.online_count}, max_players={self.max_players}, "
                f"players={self.players})")