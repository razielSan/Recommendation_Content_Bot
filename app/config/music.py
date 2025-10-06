from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class MusicSettingsDiscogs(BaseSettings):
    """Настройки для сайта https://www.discogs.com/."""

    KEY: str
    SECRET: str
    TITLE: Optional[str] = None
    ARTISTS_NAME: Optional[str] = None
    ALBUM_URL: Optional[str] = None
    FORMATS: Optional[str] = None
    RELEASED: Optional[str] = None
    COUNTRY: Optional[str] = None
    STYLES: Optional[str] = None
    TRACKLIST: Optional[str] = None
    IMG: Optional[str] = None
    URL_SEARCH: str = "https://api.discogs.com/database/search"

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="env/.env.music", extra="ignore"
    )


class MusicSettings(BaseSettings):
    """Настройки для музыкальных рекомендаций."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="env/.env.music", extra="ignore"
    )


discogs_setting: MusicSettingsDiscogs = MusicSettingsDiscogs()
music_settings: MusicSettings = MusicSettings()
