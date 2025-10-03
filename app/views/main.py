from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "/start")
async def main(message: Message):
    """Отправляет пользователю клавиатура с вариантами выбора рекомендаций."""
    await message.answer("OK")
