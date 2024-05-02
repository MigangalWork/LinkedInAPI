from configparser import ConfigParser

def get_config() -> ConfigParser:
    config: ConfigParser = ConfigParser()
    config.read('src/config.conf')
    return config