import asyncio

from dotenv import load_dotenv
from commands.dev_and_fun import init_dev
from aiogram import Bot, Dispatcher
from os import getenv

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")

dp = Dispatcher()

#Инициализацию команд вписывать сюда
init_dev(dp)

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          