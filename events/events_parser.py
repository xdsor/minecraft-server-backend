import re
from datetime import datetime

from common.utils.fsutils import load_log_file


def parse_last_events():
    events = []
    raw_logs = load_log_file()
    for log in raw_logs:
        event = _parse_log_line(log)
        if event:
            events.append(event)

    return events

def _parse_advancement(player, event_desc):
    advancement = event_desc.split("has made the advancement ")[1].replace("[", "").replace("]", "")
    return {"description": f'получил достижение "{advancement}"'}

def _parse_swim_in_lava_event(player, event_desc):
    return {"description": "утонул в лаве"}

def _parse_join_event(player, event_desc):
    return {"description": "зашел в игру"}


def _parse_leave_event(player, event_desc):
    return {"description": "вышел из игры"}


def _parse_drowned_event(player, event_desc):
    return {"description": "утонул"}


def _parse_fell_event(player, event_desc):
    return {"description": "упал с высоты"}


def _parse_slain_event(player, event_desc):
    mob = event_desc.split("was slain by ")[1]
    return {"description": f"убит существом {mob}"}


def _parse_log_line(line):
    pattern = r"\[(\d{2}:\d{2}:\d{2})\] \[Server thread/INFO\]: (\w+) (.+)"
    match = re.match(pattern, line)

    if not match:
        return None

    time_str, player, event_desc = match.groups()

    today = datetime.now().date()
    time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M:%S").timestamp()

    for keyword in event_handlers:
        if keyword in event_desc:
            handler = event_handlers[keyword]
            event_data = handler(player, event_desc)
            event_data.update({"time": time, "player": player})
            return event_data

    return None

event_handlers = {
    "has made the advancement": _parse_advancement,
    "tried to swim in lava": _parse_swim_in_lava_event,
    "joined the game": _parse_join_event,
    "left the game": _parse_leave_event,
    "drowned": _parse_drowned_event,
    "fell from a high place": _parse_fell_event,
    "was slain by": _parse_slain_event,
}