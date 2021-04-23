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
