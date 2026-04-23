import sys
sys.path.append("./src")

import asyncio
import time
import redis
import html as html_py
import re

from bs4 import BeautifulSoup, Comment
from utils import kb
from aiogram import Bot, html
from aiogram.enums import ParseMode
from loguru import logger
from common.utils.tickets_api import TicketsAPI
from common.utils.config import config

TOKEN = config['telegram_token']
CHAT_ID = config['chat_id']
CHAT_THREAD = config['chat_thread']

#Redis
REDIS_URL = config['redis_url']
REDIS_PORT = config['redis_port']

r = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    decode_responses=True,
    db=0
)

bot = Bot(TOKEN)


def clean_ms_word_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    for tag in soup.find_all(True):
        tag.attrs = {name: value for name, value in tag.attrs.items() 
                     if not name.startswith('mso-')}
        
    return soup.prettify()

def format_text(text):
    return re.sub(r'<[^>]+>', '', text)

async def mention_new_ticket(tickets):
    for ticket in tickets:
        if r.sismember("tickets:new", ticket.ticket_id):
            continue
        description_raw = clean_ms_word_html(ticket.description)[:3500] + "..."
        description = html.expandable_blockquote(html_py.escape(format_text(description_raw)).strip())

        msg = f'''🟢 Новый тикет 🟢\n\n{html.bold("ID:")} {html.link(html.bold(ticket.ticket_id), f"{config['youtrack']['url']}/tickets/{ticket.ticket_id}")}\
                \n\n{html.bold("Название")}: {html_py.escape(format_text(ticket.name))}\
                \n\
                \n@ntl_support\
                \n{description}
            '''
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML, reply_markup=await kb.spam_button(ticket.ticket_id), reply_to_message_id=CHAT_THREAD)
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