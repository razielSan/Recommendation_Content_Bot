from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройка приложения."""

    TOKEN: str

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")


settings: AppSettings = AppSettings()
