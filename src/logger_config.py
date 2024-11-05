import logging
import os
import tomllib
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from flask import has_request_context, request
from pythonjsonlogger.jsonlogger import JsonFormatter

from src.common.common_constants import CONFIG_PATH_ENV_VARIABLE, LOGS_DIR

CONFIG_PATH = os.environ.get(CONFIG_PATH_ENV_VARIABLE)

class RequestFormatter(JsonFormatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

def set_up_logging():
    logs_dir = None
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)
        logs_dir = data.get(LOGS_DIR)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    json_formatter = RequestFormatter("%(asctime)s %(name)s %(levelname)s %(url)s %(message)s")

    console_handler = StreamHandler()
    file_handler = RotatingFileHandler(
        f"{logs_dir}/backend.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=5  # Keep up to 5 archived logs
    )

    file_handler.setFormatter(json_formatter)
    console_handler.setFormatter(json_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)