import yaml


def load_config(file_config='config.yml'):
    with open(file_config, 'r') as ymlfile:
        return yaml.safe_load(ymlfile)
