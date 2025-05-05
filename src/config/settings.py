"""
This file contains the class for managing the settings
"""

from pydantic import BaseModel
from pydantic_settings import (BaseSettings, SettingsConfigDict,
                               YamlConfigSettingsSource)


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_URI: str


class StorageSettings(BaseModel):
    base_path: str
    raw_zone: str
    processed_zone: str
    refined_zone: str


class YamlSettings(BaseSettings):
    model_config = SettingsConfigDict(yaml_file="config.yaml")
    storage: StorageSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (YamlConfigSettingsSource(settings_cls),)


class Settings:
    def __init__(self):
        self.environment_settings = EnvironmentSettings()
        self.yaml_settings = YamlSettings()
