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
