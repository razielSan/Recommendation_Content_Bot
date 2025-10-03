import asyncio

from extensions import bot, dp
from config.settings import settings


async def on_statup() -> None:
    """Функция срабатывает при старте бота."""
    print("Бот запущенн")


async def main() -> None:
    """Главная функция."""
    await bot.set_my_commands(commands=settings.BOT_COMMAND)
    await bot.delete_webhook(drop_pending_updates=True)

    dp.startup.register(on_statup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
