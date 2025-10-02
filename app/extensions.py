from aiogram import Bot, Dispatcher

from config.settings import settings


bot: Bot = Bot(token=settings.TOKEN)
dp: Dispatcher = Dispatcher()
