from dataclasses import dataclass
import json
from pathlib import Path
from loguru import logger


@logger.catch
def init_config():
    config_file_path = Path("config.json").resolve()
    with open(config_file_path) as f:
        config_file = f.read()
    config_json = json.loads(config_file)
    return Config(**config_json)


@dataclass
class Config:
    env: str
    ldap_server: str
    ldap_user: str
    ldap_password: str
    discord_token: str

    def __post_init__(self):
        logger.info(f'loading config with "{self.env}" environment.')


config = init_config()
