import sys
sys.path.append("./src")

import asyncio
import time
import redis
import html as html_py
import re

from utils import kb
from aiogram import Bot, html
from aiogram.enums import ParseMode
from loguru import logger
from common.utils.tickets_api import TicketsAPI
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")

#Redis
REDIS_URL = getenv("REDIS_URL")
REDIS_PORT = getenv("REDIS_PORT")

r = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    decode_responses=True,
    db=0
)

bot = Bot(TOKEN)

def format_text(text):
    return re.sub(r'<[^>]+>', '', text)

#TODO: Сделать кнопку спама
async def mention_new_ticket(tickets):
    for ticket in tickets:
        if r.sismember("tickets:new", ticket.ticket_id):
            continue
        msg = f'''🟢 Новый тикет 🟢\n\n{html.bold("ID:")} {html.link(html.bold(ticket.ticket_id), f"https://tracker.ntechlab.com/tickets/{ticket.ticket_id}")}\
                \n\n{html.bold("Название")}: {format_text(ticket.name)}\
                \n\
                \n@ntl_support\
                \n{html.expandable_blockquote(format_text(ticket.description))}
            '''
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML, reply_markup=await kb.spam_button(ticket.ticket_id))
        logger.info(f"Ticket {ticket.ticket_id} mentioned.")
        r.sadd("tickets:new", ticket.ticket_id)
        


async def polling():
    api = TicketsAPI()
    while True:
        tickets = api.get_new_ticket()
        if len(tickets) != 0:
            logger.debug(f"len of tickets arr: ({len(tickets)})")
            await mention_new_ticket(tickets)
        else:
            logger.info(f"No new tickets.")
            logger.debug(f"len of tickets arr: ({len(tickets)})")
        time.sleep(100)

if __name__ == "__main__":
    asyncio.run(polling())