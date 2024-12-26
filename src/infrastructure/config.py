import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    ENVIRONMENT: str = Field(default="local", env="ENVIRONMENT")
    INITIAL_DOCUMENTS_PATH: str = Field(default="data/input", env="INITIAL_DOCUMENTS_PATH")

    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_EMB_DEPLOYMENT_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    @classmethod
    def load(cls) -> "Settings":
        """
        Load configuration settings from both a .env file and a dynamically determined YAML file.

        Environment variables defined in the .env file take precedence over those in the YAML file. 
        The YAML file is used to load additional settings not specified in the .env file.
        """
        env_settings = cls()
        environment = env_settings.ENVIRONMENT

        yaml_file_path = f"config/{environment}/config.yml"
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError(f"Configuration file not found: {yaml_file_path}")

        with open(yaml_file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
        
        yaml_data.update(env_settings)

        return cls(**yaml_data)


config = Settings.load()
