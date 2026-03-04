import yaml

from datetime import datetime, timezone, timedelta

from aiogram.filters import BaseFilter

from aiogram import types
from loguru import logger

try:
    with open('config/settings.yaml', 'r', encoding="utf-8") as data:
        config = yaml.load(data, Loader=yaml.FullLoader)

    logger.info("YAML config successfully loaded.")
except Exception as e:
    logger.error(f"Error while loading YAML: {e}")


class isSupportTeam(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.username in str(config['users-support-team'])
    
class isTimeToUpdate(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        now = datetime.now(timezone(timedelta(hours=3))).strftime("%H")
        block_hours = list(range(9, 21, 1))
        if (int(now) in block_hours):
            await message.answer("Обновление доступно только с 21:00 до 8:00")
        return int(now) not in block_hours