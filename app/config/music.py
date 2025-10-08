from typing import Optional, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class MusicSettingsDiscogs(BaseSettings):
    """Настройки для сайта https://www.discogs.com/."""

    DICT_STYLES: dict = {
        "Punk": "Punk",
        "Hardcore": "Hardcore",
        "Crust": "Crust",
        "Grindcore": "Grindcore",
        "Post-Punk": "Post-Punk",
        "Heavy Metal": "Heavy Metal",
        "Thrash": "Thrash",
        "Crossover thrash": "Crossover thrash",
        "Black Metal,": "Black Metal,",
        "Death Metal": "Death Metal",
    }

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
    TRACKLIST: Optional[int] = None
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
