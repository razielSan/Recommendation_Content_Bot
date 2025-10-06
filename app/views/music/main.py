from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from config.music import music_settings
from keyboards.music.inline import get_music_main_button

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == music_settings.MUSIC)
async def main(message: Message):
    await message.answer(
        text="Доступные варианты",
        reply_markup=get_music_main_button(),
    )
