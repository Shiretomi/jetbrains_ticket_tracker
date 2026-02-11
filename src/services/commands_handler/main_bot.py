import sys
sys.path.append("./src")

from dotenv import load_dotenv
from commands.dev_and_fun import init_dev
from commands.callbacks import init_callbacks
from aiogram import Bot, Dispatcher
from os import getenv

import asyncio


load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")

BOT = Bot(token=TOKEN)

dp = Dispatcher()

#Инициализацию команд вписывать сюда
init_dev(dp)
init_callbacks(dp)

async def main() -> None:
    await dp.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
          