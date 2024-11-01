import logging

from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from common.common_constants import CONFIG_PATH_ENV_VARIABLE
from events.routes import events_bp
from players.routes import players_bp
from stats.routes import stats_bp

app = Flask(__name__)
app.config.from_envvar(CONFIG_PATH_ENV_VARIABLE)
app.logger.setLevel(logging.INFO)
logging.root.setLevel(logging.INFO)
CORS(app)
metrics = PrometheusMetrics(app)

app.register_blueprint(players_bp, url_prefix='/api/players')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(stats_bp, url_prefix='/api/stats')

if __name__ == '__main__':
    app.run()
