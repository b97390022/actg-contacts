import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from loguru import logger

from src.utils import get_file_path


@logger.catch
def init_config(file_path: str, obj: Any):
    config_file_path = Path(file_path).resolve()
    with open(config_file_path, encoding='utf-8') as f:
        config_file = f.read()
    config_json = json.loads(config_file)
    return obj(**config_json)


@dataclass
class EnvConfig:
    contact_src_path: str


@dataclass
class Config:
    env: str
    env_config: EnvConfig = field(init=False)
    ldap_server: str
    ldap_user: str
    ldap_password: str
    discord_token: str
    smb_user: str
    smb_password: str

    def __post_init__(self):
        logger.info(f'loading config with "{self.env}" environment')
        logger.info('initiate env specific config')
        match self.env:
            case 'dev' | 'develop' | 'development':
                env_config_name = get_file_path(".", "dev.json")
            case 'prod' | 'production':
                env_config_name = get_file_path(".", "prod.json")
            case _:
                env_config_name = get_file_path(".", "dev.json")
        self.env_config = init_config(env_config_name, EnvConfig)


config: Config = init_config(get_file_path(".", "config.json"), Config)
