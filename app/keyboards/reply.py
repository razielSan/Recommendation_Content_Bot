from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton

from config.music import music_settings


def get_main_menu_button():
    """Возвращает клавиатуру с кнопками главного меню

    Returns:
        _type_: reply_keyboard
    """
    reply_kb = ReplyKeyboardBuilder(
        markup=[
            [
                KeyboardButton(text=music_settings.MUSIC),
            ],
        ],
    )
    return reply_kb.as_markup(resize_keyboard=True)


def get_cancel_button():
    reply_kb = ReplyKeyboardBuilder(
        markup=[
            [
                KeyboardButton(text="Отмена"),
            ],
        ],
    )
    return reply_kb.as_markup(resize_keyboard=True)
