import requests
import time
from typing import Dict, List
from collections.abc import Callable

from config.music import discogs_setting, MusicSettingsDiscogs


def get_list_albums_for_discogs(
    style: str,
    per_page: int,
    url: str,
    year: int,
    cancel_check: Callable,
    update_progress: Callable,
) -> List:
    """Возвращает список альбомов исполнителей по жанру для сайта discogs.com

    Args:
        style (str): Стиль альбома
        per_page (int): Количество альбомов
        url (str): URL для поиска

    Returns:
        _type_: Возвращает список альбомов исполнителей по жанру для сайта discogs.com
    """
    params: Dict = {
        "key": discogs_setting.KEY,
        "secret": discogs_setting.SECRET,
        "style": discogs_setting.DICT_STYLES[style],
        "year": year,
        "format": "Album",
        "per_page": per_page,
        "page": 1,
        "sort": "year",
        "sort_order": "desc",
    }

    response = requests.get(url=url, params=params).json()

    list_artists: List = []

    for result in response["results"]:
        master_url: str = result["master_url"]
        try:
            if master_url:
                # Проверяет на состояние отмены запроса
                if cancel_check():
                    return []

                response = requests.get(url=master_url, timeout=100).json()

                time.sleep(2)

                main_release_url = response["main_release_url"]

                # Проверяет на состояние отмены запроса
                if cancel_check():
                    return []
                response = requests.get(url=main_release_url, timeout=100).json()
                time.sleep(2)
            else:
                # Проверяет на состояние отмены запроса
                if cancel_check():
                    return []
                response = requests.get(url=result["resource_url"], timeout=100).json()
                time.sleep(2)

            # Проверяет на состояние отмены запроса
            if cancel_check():
                return []
            tracklist: int = len(response["tracklist"])

            music: MusicSettingsDiscogs = discogs_setting.model_validate(
                {
                    "TITLE": response["title"],
                    "ARTISTS_NAME": response["artists"][0]["name"],
                    "ALBUM_URL": response["uri"],
                    "FORMATS": ", ".join(response["formats"][0]["descriptions"]).strip(
                        ", "
                    ),
                    "RELEASED": response["released"],
                    "COUNTRY": response["country"],
                    "STYLES": ", ".join(response["styles"]).strip(", "),
                    "TRACKLIST": tracklist,
                    "IMG": response["images"][0]["uri150"],
                }
            )
            # Обновляем прогресс скачивания
            update_progress()
            list_artists.append(music)
        except Exception as err:
            print(err)

    list_artists.sort(key=lambda x: x.dict()["RELEASED"])

    return list_artists[::-1]


def get_descripions_for_albums(album: Dict) -> str:
    """Возвращает строку с информацией об альбоме

    Args:
        album (Dict): словарь с данными об альбоме

    Returns:
        _type_: Возвращает строку с информацией об альбоме
    """
    data: str = ""
    data += f'{album["ARTISTS_NAME"]}\n\n'
    data += f"Страна: {album['COUNTRY']}\n"
    data += f"Название альбома: {album['TITLE']}\n"
    data += f"Формат {album['FORMATS']}\n"
    data += f"Жанры: {album['STYLES']}\n"
    data += f"Дата выхода: {album['RELEASED']}\n\n"
    data += f"Количество песне в альбоме: {album['TRACKLIST']}\n\n"
    data += album["ALBUM_URL"]

    return data
