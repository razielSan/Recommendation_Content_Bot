from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from config.music import music_settings
from keyboards.music.inline import get_music_main_button, get_main_musical_news_button


router = Router(name=__name__)


@router.callback_query(StateFilter(None), F.data == music_settings.CALLBACK_MUSIC_NEWS)
async def main(call: CallbackQuery):
    await call.message.answer(
        text="Доступные варианты",
        reply_markup=get_main_musical_news_button(),
    )
