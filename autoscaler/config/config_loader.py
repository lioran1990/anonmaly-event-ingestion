import os


class ConfigLoader:
    def __init__(self, config_file='config.env'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        config = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                for line in file:
                    name, value = line.strip().split('=', 1)
                    config[name] = value
        else:
            config['RABBITMQ_API'] = os.getenv('RABBITMQ_API', 'rabbitmq')
            config['RABBITMQ_USER'] = os.getenv('RABBITMQ_USER', 'guest')
            config['RABBITMQ_PASSWORD'] = os.getenv('RABBITMQ_PASSWORD', 'guest')
            config['RABBITMQ_QUEUE'] = os.getenv('RABBITMQ_QUEUE', 'cloudtrail')
            config['SCALE_UP_THRESHOLD'] = os.getenv('SCALE_UP_THRESHOLD', '10')
            config['SCALE_DOWN_THRESHOLD'] = os.getenv('SCALE_DOWN_THRESHOLD', '2')
            config['MIN_WORKERS'] = os.getenv('MIN_WORKERS', '1')
            config['MAX_WORKERS'] = os.getenv('MAX_WORKERS', '10')
            config['CHECK_INTERVAL'] = os.getenv('CHECK_INTERVAL', '3')
        return config
