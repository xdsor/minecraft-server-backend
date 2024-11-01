from flask import Blueprint, Response

from common.utils.fsutils import read_user_stats
from common.username_id_mappings import user_name_id_mapping
from stats.business import get_server_time, get_all_stats

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('', methods=['GET'])
def handle_get_all_stats():
    return get_all_stats()

@stats_bp.route('/<user_name>', methods=['GET'])
def get_user_stats(user_name):
    user_id = user_name_id_mapping.get(user_name)
    if user_id:
        return read_user_stats(user_id)
    else:
        return Response(status=404)

@stats_bp.route('/server/time', methods=['GET'])
def handle_get_server_time():
    return get_server_time()