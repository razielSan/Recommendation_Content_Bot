import asyncio

from extensions import bot, dp
from config.settings import settings
from views.main import router as main_router
from views.music.main import router as music_main_router
from views.music.musical_news.main import router as musical_news_main_router
from views.music.musical_news.discogs.main import router as discogs_main_router


async def on_statup() -> None:
    """Функция срабатывает при старте бота."""
    print("Бот запущенн")


async def main() -> None:
    """Главная функция."""
    await bot.set_my_commands(commands=settings.BOT_COMMAND)
    await bot.delete_webhook(drop_pending_updates=True)

    dp.startup.register(on_statup)
    dp.include_router(discogs_main_router)
    dp.include_router(musical_news_main_router)
    dp.include_router(music_main_router)
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
