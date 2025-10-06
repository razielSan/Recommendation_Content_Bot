from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from keyboards.reply import get_main_menu_button


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "/start")
async def main(message: Message):
    """Отправляет пользователю клавиатура с вариантами выбора рекомендаций."""
    print("ok")
    await message.answer(
        text="Доступные варианты",
        reply_markup=get_main_menu_button(),
    )
