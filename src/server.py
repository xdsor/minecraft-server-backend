import logging
import os

from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from src.common.common_constants import CONFIG_PATH_ENV_VARIABLE
from src.events.routes import events_bp
from src.logger_config import set_up_logging
from src.players.routes import players_bp
from src.stats.routes import stats_bp

def create_app():
    set_up_logging()

    app = Flask(__name__)
    if os.environ.get(CONFIG_PATH_ENV_VARIABLE):
        app.config.from_envvar(CONFIG_PATH_ENV_VARIABLE)

    CORS(app)
    PrometheusMetrics(app)

    app.register_blueprint(players_bp, url_prefix='/api/players')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')

    app.logger.info(f"Server object is created!")
    return app
