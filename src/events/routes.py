import json

from flask import Blueprint, Response

from src.events.events_parser import parse_last_events

events_bp = Blueprint('events', __name__)

@events_bp.route('', methods=['GET'])
def load_server_events():
    return Response(json.dumps(parse_last_events(), ensure_ascii=False), content_type='application/json; charset=utf-8')