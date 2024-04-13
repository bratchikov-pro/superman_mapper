import os
from pprint import pprint

import dataclass_factory
import yaml

from dataclasses import dataclass
from typing import List, Dict


# TODO: Написать метод run() -- инициализираует все сервисы и бота из конфига, будет использоваться в main

@dataclass
class Category:
    name: str
    amenities: List[str]


@dataclass
class RedisConfiguration:
    host: str
    port: int
    database: int
    username_env_name: str
    password_env_name: str

    username: str = ""
    password: str = ""

    def __post_init__(self):
        self.username = os.environ.get(self.username_env_name)
        self.password = os.environ.get(self.password_env_name)


@dataclass
class OSMConfiguration:
    categories_to_amenities_map: Dict[str, Category]


@dataclass
class TelegramBotConfiguration:
    token_env_name: str
    workers_count: int

    bot_token: str = ""

    def __post_init__(self):
        self.bot_token = os.environ.get(self.token_env_name)


@dataclass
class Config:
    osm_broker: OSMConfiguration
    redis: RedisConfiguration
    telegram_bot: TelegramBotConfiguration


def load_config():
    with open('config.yaml', 'r') as stream:
        yaml_config = yaml.safe_load(stream)

        factory = dataclass_factory.Factory()
        config: Config = factory.load(yaml_config, Config)

        pprint(config)
