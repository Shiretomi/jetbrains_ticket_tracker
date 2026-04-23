import sys
sys.path.append("./src")

from commands.dev_and_fun import init_dev
from commands.callbacks import init_callbacks
from commands.ansible import init_ansible
from commands.scripts import init_scripts
from aiogram import Bot, Dispatcher
from common.utils.config import config

import asyncio

TOKEN = config['telegram_token']

BOT = Bot(token=TOKEN)

dp = Dispatcher()

#Инициализацию команд вписывать сюда
init_dev(dp)
init_callbacks(dp)
init_ansible(dp)
init_scripts(dp)

async def main() -> None:
    await dp.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
          