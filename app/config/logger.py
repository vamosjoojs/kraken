import logging
import uuid

import boto3
import watchtower

from app.config.config import config

client = boto3.client(
    "logs",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name="us-east-2",
)

logging.basicConfig(level=logging.INFO)

cloud_watch_handler = watchtower.CloudWatchLogHandler(
    log_group="kraken",
    boto3_client=client,
    send_interval=5,
    log_stream_name=f"{str(uuid.uuid4())}",
)


class Logger:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.addHandler(cloud_watch_handler)
        return logger
