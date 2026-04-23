from datetime import datetime, timezone, timedelta
from aiogram.filters import BaseFilter
from aiogram import types
from .config import config

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