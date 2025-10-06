from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class MusicSettingsDiscogs(BaseSettings):
    """Настройки для сайта https://www.discogs.com/."""

    DISCOGS: str = "🎵 Discogs 🎵"  # Отображение надписи в мызыкальных новинках
    CALLBACK_DISCOGS: str = "discogs"  # callback отображение

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

    MUSIC: str = "🎧 Mузыка 🎧"  # Отображение надписи в главном меню

    MUSIC_NEWS: str = (
        "🤘 Музыкальные Новинки 🤘"  # Отображение надписи в музыкальном меню
    )
    CALLBACK_MUSIC_NEWS: str = "musical_news"  # callback отображение

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="env/.env.music", extra="ignore"
    )


discogs_setting: MusicSettingsDiscogs = MusicSettingsDiscogs()
music_settings: MusicSettings = MusicSettings()
