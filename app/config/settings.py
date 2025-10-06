from typing import List

from aiogram.types import BotCommand

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    TOKEN: str
    BOT_COMMAND: List[BotCommand] = [
        BotCommand(command="start", description="Меню бота")
    ]

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="env/.env",
        extra="ignore"
    )


settings: AppSettings = AppSettings()
