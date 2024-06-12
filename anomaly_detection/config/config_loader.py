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
            config['POSTGRES_DB'] = os.getenv('POSTGRES_DB', 'mydb')
            config['POSTGRES_USER'] = os.getenv('POSTGRES_USER', 'postgres')
            config['POSTGRES_PASSWORD'] = os.getenv('POSTGRES_PASSWORD', 'pass')
            config['POSTGRES_HOST'] = os.getenv('POSTGRES_HOST', 'to delete')
        return config
