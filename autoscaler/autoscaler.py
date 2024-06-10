import requests
import time
import docker
import logging

from config.config_loader import ConfigLoader

# Configuration
config = ConfigLoader().load_config()
RABBITMQ_API = config.get('RABBITMQ_API')
RABBITMQ_USER = config.get('RABBITMQ_USER')
RABBITMQ_PASS = config.get('RABBITMQ_PASSWORD')
SCALE_UP_THRESHOLD = int(config.get('SCALE_UP_THRESHOLD'))
SCALE_DOWN_THRESHOLD = int(config.get('SCALE_DOWN_THRESHOLD'))
MIN_WORKERS = int(config.get('MIN_WORKERS'))
MAX_WORKERS = int(config.get('MAX_WORKERS'))
CHECK_INTERVAL = int(config.get('CHECK_INTERVAL'))  # seconds

# Initialize Docker client
client = docker.from_env()


def get_queue_length() -> int:
    try:
        response = requests.get(RABBITMQ_API, auth=(RABBITMQ_USER, RABBITMQ_PASS))
        response.raise_for_status()
        data = response.json()
        logging.info(f"RabbitMQ API response: {data}")
        return data.get('messages', 0)
    except requests.RequestException as e:
        logging.error(f"Error getting queue length: {e}")
        return 0


def scale_workers(service_name, replica_count) -> None:
    try:
        service = client.services.get(service_name)
        service.update(mode={"Replicated": {"Replicas": replica_count}})
        logging.info(f"Scaled {service_name} to {replica_count} replicas")
    except docker.errors.APIError as e:
        logging.error(f"Error scaling service {service_name}: {e}")


def main():
    service_name = 'my_stack_worker'

    while True:
        queue_length = get_queue_length()
        logging.info(f"Queue length: {queue_length}")

        try:
            service = client.services.get(service_name)
            current_replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
            new_replicas = current_replicas

            if queue_length > SCALE_UP_THRESHOLD and current_replicas < MAX_WORKERS:
                new_replicas = current_replicas + 1
            elif queue_length < SCALE_DOWN_THRESHOLD and current_replicas > MIN_WORKERS:
                new_replicas = current_replicas - 1

            if new_replicas != current_replicas:
                logging.info(f"Scaling workers from {current_replicas} to {new_replicas}")
                scale_workers(service_name, new_replicas)

        except docker.errors.APIError as e:
            logging.error(f"Error retrieving service info: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
