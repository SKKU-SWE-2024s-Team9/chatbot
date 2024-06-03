from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_url: str = "localhost:3000"
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env")
