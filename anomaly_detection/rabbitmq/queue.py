from anomaly_detection.utils.logger import logger
from datetime import time

import pika

QUEUE_NAME = 'cloudtrail'
RABBITMQ_HOST = 'rabbitmq'


def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            logger.info("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Could not connect to RabbitMQ: {e}. Retrying in 5 seconds...")
            time.sleep(5)


def get_queue_connection(queue_name: str):
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return channel


def start_queue(callback):
    channel = get_queue_connection(queue_name=QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
