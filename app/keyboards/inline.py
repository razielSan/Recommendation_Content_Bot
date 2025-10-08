from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


def get_button_for_forward_or_back(
    list_albums: List,
    count: int = 0,
    step: int = 1,
):
    """Возвращает инлайн кнопки для прoлистывания назад или вперед."""

    inline_kb = InlineKeyboardBuilder()
    if count == 0:
        if len(list_albums) == 1:
            pass
        else:
            inline_kb.add(
                InlineKeyboardButton(
                    text="Вперед 👉", callback_data=f"discogs forward {count+step}"
                )
            )
    else:
        if len(list_albums) - count == step:
            inline_kb.add(
                InlineKeyboardButton(
                    text="👈 Назад", callback_data=f"discogs back {count-step}"
                )
            )
        elif len(list_albums) - count >= step:
            inline_kb.add(
                InlineKeyboardButton(
                    text="👈 Назад", callback_data=f"discogs back {count-step}"
                )
            )
            inline_kb.add(
                InlineKeyboardButton(
                    text="Вперед 👉", callback_data=f"discogs forward {count+step}"
                )
            )
    return inline_kb.as_markup(resize_keyboard=True)
