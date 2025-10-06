from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from config.music import discogs_setting


router = Router(name=__name__)


@router.callback_query(StateFilter(None), F.data == discogs_setting.CALLBACK_DISCOGS)
async def main(call: CallbackQuery):
    print("ok")
    await call.message.answer("ok")
