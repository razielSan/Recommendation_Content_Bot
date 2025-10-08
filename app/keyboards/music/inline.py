from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from config.music import music_settings, discogs_setting


def get_music_main_button():
    """Возвращает кнопки с выбором вариантов музыкальных рекомендаций.

    Returns:
        _type_: inline_kb
    """
    inline_kb = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(
                    text=music_settings.MUSIC_NEWS,
                    callback_data=music_settings.CALLBACK_MUSIC_NEWS,
                )
            ],
        ]
    )
    return inline_kb.as_markup(resize_keyboard=True)


def get_main_musical_news_button():
    """Возвращает инлайн кнопки меню музыкальных новинок

    Returns:
        _type_: inline_kb
    """
    inline_kb = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(
                    text=discogs_setting.DISCOGS,
                    callback_data=discogs_setting.CALLBACK_DISCOGS,
                )
            ],
        ]
    )
    return inline_kb.as_markup(resize_keyboard=True)


def get_discogs_menu_button():
    """Возвращает инлайн кнопки меню выбора музыкальных новинок для сайта discogs.com

    Returns:
        _type_: inline_kb
    """
    inline_kb = InlineKeyboardBuilder()
    for index, genre in enumerate(discogs_setting.DICT_STYLES.values(), start=0):
        if index % 3 == 0:
            inline_kb.row(
                InlineKeyboardButton(
                    text=genre,
                    callback_data=f"GenreDiscogs_{genre}",
                )
            )
        else:
            inline_kb.add(
                InlineKeyboardButton(
                    text=genre,
                    callback_data=f"GenreDiscogs_{genre}",
                )
            )

    return inline_kb.as_markup(resize_keyboard=True)
