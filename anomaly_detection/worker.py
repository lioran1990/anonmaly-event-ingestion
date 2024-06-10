import json
import random
import time
from datetime import datetime
from typing import Optional

from anomaly_detection.config.config_loader import ConfigLoader
from anomaly_detection.db.database import Database
from anomaly_detection.decorator.transaction import transaction

from anomaly_detection.utils.logger import logger
from anomaly_detection.models.anomaly import Anomaly
from anomaly_detection.rabbitmq.queue import start_queue


def map_event_to_anomaly(event):
    event_timestamp = datetime.fromtimestamp(int(event.get('event_timestamp')))
    return {
        'request_id': event.get('request_id'),
        'event_id': event.get('event_id'),
        'role_id': event.get('role_id'),
        'event_type': event.get('event_type'),
        'event_timestamp': event_timestamp,
        'affected_assets': event.get('affected_assets'),
    }


def detect_anomaly():
    # simulate anomaly score
    return random.random()


@transaction
def get_event_from_db(session, event_id: str) -> Optional[Anomaly]:
    existing_event = session.query(Anomaly).filter_by(event_id=event_id).first()
    return existing_event


@transaction
def save_anomaly(session, anomaly_data: dict) -> None:
    session.add(Anomaly(**anomaly_data))
    logger.info(f"Saving anomaly: {anomaly_data}")


def process_event(ch, method, properties, body) -> None:
    time.sleep(3)  # Simulate processing time, 3 seconds

    logger.info("Processing event...")
    event = json.loads(body)
    try:
        anomaly_data = map_event_to_anomaly(event)
        event_id = anomaly_data['event_id']
    except KeyError as e:
        logger.error(f"Invalid event: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    logger.info(f"Received event ID: {event_id}")

    existing_event = get_event_from_db(event_id)
    if not existing_event:
        anomaly_score = detect_anomaly()
        if anomaly_score > 0:
            logger.info(f"Detected anomaly: {event_id}, score: {anomaly_score}")
            anomaly_data["score"] = anomaly_score
            save_anomaly(anomaly_data=anomaly_data)
    else:
        logger.info(f"Anomaly already detected for event in the database, skipping: {event_id}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def get_db_url(config: dict):
    logger.info(f"Connecting to database: {config['POSTGRES_DB']}"
                f" on host: {config['POSTGRES_HOST']}"
                f" with user: {config['POSTGRES_USER']}"
                )
    return f"postgresql+psycopg2://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@{config['POSTGRES_HOST']}/{config['POSTGRES_DB']}"


if __name__ == '__main__':
    logger.info("Starting worker...")

    logger.info("Loading configuration...")
    config = ConfigLoader().load_config()

    logger.info("Initializing database...")

    db = Database(get_db_url(config))

    logger.info("Starting queue...")
    start_queue(process_event)
