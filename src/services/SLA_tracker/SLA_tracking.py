import sys
sys.path.append("./src")

from aiogram import Bot, html
from aiogram.enums import ParseMode
from os import getenv
from dotenv import load_dotenv
from loguru import logger
from common.utils.tickets_api import TicketsAPI
from common.models.ticket import Ticket
from datetime import datetime as dt 

import redis
import urllib3
import asyncio
import time

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Telegram
TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")
CHAT_THREAD = getenv("CHAT_THREAD")

#Redis
REDIS_URL = getenv("REDIS_URL")
REDIS_PORT = getenv("REDIS_PORT")

bot = Bot(TOKEN)

r = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    decode_responses=True,
    db=1
)

async def mention_broken_SLA(tickets):
    try:
        for ticket in tickets:
            print(ticket)
            if r.sismember("tickets:known", ticket):
                continue
            else:
                user_ping = ""
                ticket = Ticket.from_youtrack(ticket)
                msg = f'''🔴 SLA просрочен 🔴\
                            \n\
                            \n{html.link(html.bold(ticket.ticket_id), f"https://tracker.ntechlab.com/tickets/{ticket.ticket_id}")}\
                            \n\
                            \n{ticket.name}\
                            \n\
                            \n@ntl_support\n{user_ping}\
                            '''
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML, reply_to_message_id=CHAT_THREAD)
                r.sadd("tickets:known", ticket.ticket_id)

    except Exception as e:
        print(ticket)
        logger.error(f"Ticket: {ticket.ticket_id} Error {e}.")
        await bot.send_message(chat_id=CHAT_ID, text=f"🔴 SLA просрочен 🔴\nОшибка с тикетом {ticket.ticket_id}\nНе удалось спарсить", parse_mode=ParseMode.HTML, reply_to_message_id=CHAT_THREAD)
        r.sadd("tickets:known", ticket.ticket_id)
        await mention_broken_SLA(tickets)

async def polling():
    api = TicketsAPI()
    while True:
        tickets = api.get_tickets_info_for_sla_check()
        sla_broken = []
        for ticket in tickets:
            sla = int(int(ticket.SLA_ends)/1000) - int(dt.now().timestamp())
            if sla == int(dt.now().timestamp()) * -1:
                pass
            elif sla < 0 and not r.sismember("tickets:known", ticket.ticket_id):
                sla_broken.append(ticket.ticket_id)
        
        
        if len(sla_broken) != 0:
            logger.info(f"{len(sla_broken)} tickets with broken SLA.")
            await mention_broken_SLA(sla_broken)
        else:
            logger.info(f"No new broken SLA.")
        time.sleep(600)

if __name__ == "__main__":
    asyncio.run(polling())