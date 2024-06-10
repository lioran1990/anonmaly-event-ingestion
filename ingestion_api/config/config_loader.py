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
            config['RABBITMQ_HOST'] = os.getenv('RABBITMQ_HOST', 'rabbitmq')
            config['RABBITMQ_USER'] = os.getenv('RABBITMQ_USER', 'guest')
            config['RABBITMQ_PASSWORD'] = os.getenv('RABBITMQ_PASSWORD', 'guest')
            config['RABBITMQ_QUEUE'] = os.getenv('RABBITMQ_QUEUE', 'cloudtrail')
        return config
