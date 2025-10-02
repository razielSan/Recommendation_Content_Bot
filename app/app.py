import asyncio

from extensions import bot, dp


async def on_statup():
    print("Бот запущенн")


async def main():

    dp.startup.register(on_statup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
