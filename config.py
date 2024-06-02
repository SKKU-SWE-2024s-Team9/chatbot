from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_port: str = "3000"
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env")
