import requests

from aiogram import F
from aiogram import types
from common.utils import tickets_api

API = tickets_api.TicketsAPI()

def init_callbacks(bot):
    @bot.callback_query(F.data.startswith('spam_ticket'))
    async def spam_button_callback(callback: types.CallbackQuery):
        API.send_to_spam(callback.data.split(":")[1])