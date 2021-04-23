import configparser
import os

CONFIG_PATH = 'settings.ini'


def get_config(name):
    if not os.path.exists(CONFIG_PATH):
        raise Exception('File "settings.ini" is missing')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    try:
        items = config.items(name)
    except configparser.NoSectionError as exc:
        raise Exception(f'No setting found for hostname {name}') from exc
    return dict(items, **{'name': name})

def get_path_cisco():
    path = get_config('PATH').get('path')
    if path is None:
        raise Exception('The path to cisco is not specified in the settings')
    return path



class Config:
    
    def __init__(self, name, values= {}):
        self.name = name
        self.values = values
    
    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            self.values.update({key: value})

    def create_config(self):
        config = configparser.ConfigParser()
        config.add_section(self.name)
        for key, value in self.values.items():
            config.set(self.name, key, value)
        with open(CONFIG_PATH, 'w') as config_file:
            config.write(config_file)

# host_name, login, password

if __name__ == "__main__":
    cnf = Config('SL24', {'host_name': 'https://remote3.sl24leasing.ru/', 'login': 'makhortov.d', 'password': 'TPnxV=jh4gyN'})
    #cnf = Config('SL24')
    cnf.create_config()