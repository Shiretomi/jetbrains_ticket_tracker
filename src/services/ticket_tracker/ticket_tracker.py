import sys
sys.path.append("./src")

import asyncio
import time

from aiogram import Bot, html
from aiogram.enums import ParseMode
from loguru import logger
from common.utils.tickets_api import TicketsAPI
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")

bot = Bot(TOKEN)


async def mention_new_ticket(tickets):
    for ticket in tickets:
        msg = f'''🟢 Новый тикет 🟢                         
                \n{html.link(html.bold(ticket.ticket_id), f"https://tracker.ntechlab.com/tickets/{ticket.ticket_id}")}\
                \n\
                \n{ticket.name}\
            '''
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML)
        logger.info(f"Ticket {ticket.ticket_id} mentioned.")
        


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
        time.sleep(300)

if __name__ == "__main__":
    asyncio.run(polling())