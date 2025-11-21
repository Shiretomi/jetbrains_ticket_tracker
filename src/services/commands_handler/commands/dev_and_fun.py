import requests

from loguru import logger
from aiogram import html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from common.models.ticket import Ticket
from os import getenv

def init_dev(bot):

    @bot.message(Command("chat_id"))
    async def get_chat_id(message: Message):
        await message.reply(f"ID Чата: {html.bold(message.chat.id)}\nID Треда: {html.bold(message.message_thread_id)}", parse_mode=ParseMode.HTML)

    @bot.message(Command("get_ticket"))
    async def get_ticket(message: Message):
        try:
            ticket_id = message.text.split(" ")[1]
            ticket_info = Ticket.from_youtrack(ticket_id)
            await message.answer(ticket_info.description)
        except Exception as e:
            logger.warning(e)
            await message.answer("Неверный формат.")

    @bot.message(Command("tickets_count"))
    async def tickets_count(message: Message):
        TOKEN = getenv('YOUTRACK_TOKEN')
        URL = "https://tracker.ntechlab.com/api/sortedIssues"
        ATTRIBS = "?topRoot=100&skipRoot=0&flatten=true&query=state: {Waiting for L2}, {Waiting for developer}, {Waiting for delivery}, {Waiting for customer}, {On hold}, {Waiting for support}&folderId=108-0&fields=tree(id,summaryTextSearchResult(highlightRanges(startOffset,endOffset)))"
        HEADERS = {
            'Accept': 'application/json',
            f'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
        full_url = f"{URL}{ATTRIBS}"
        tickets = requests.get(full_url, headers=HEADERS).json()["tree"]

        await message.reply(f"🌴 Всего открытых тикетов на саппорте: {html.bold(len(tickets))}", parse_mode=ParseMode.HTML)