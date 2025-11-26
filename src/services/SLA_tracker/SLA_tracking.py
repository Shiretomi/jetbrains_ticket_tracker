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

import yaml
import urllib3
import asyncio
import time

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")
bot = Bot(TOKEN)

try:
    with open('config/settings.yaml', 'r') as data:
        config = yaml.load(data, Loader=yaml.FullLoader)

    logger.info("YAML config successfully loaded.")
except Exception as e:
    logger.error(f"Error while loading YAML: {e}")

def load_known_tickets():
    try:
        with open('SLA_broken_tickets.txt', 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_new_tickets(all_tickets):    
    with open('SLA_broken_tickets.txt', 'w') as file:
        for ticket in all_tickets:
            file.write(f"{ticket}\n")
        file.close()

async def mention_broken_SLA(tickets):
    try:
        known_tickets = load_known_tickets()
        new_tickets = []
        for ticket in tickets:
            if ticket in known_tickets:
                continue
            else:
                #TODO: пинг через конфиг ямл
                new_tickets.append(ticket)
                ticket = Ticket.from_youtrack(ticket)
                msg = f'''🔴 SLA просрочен 🔴\
                            \n\
                            \n{html.link(html.bold(ticket.ticket_id), f"https://tracker.ntechlab.com/tickets/{ticket.ticket_id}")}\
                            \n\
                            \n{ticket.name}\
                            \n\
                            \n{config["users"][ticket.assignee]["tg_user"]}\
                            '''
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML)
        save_new_tickets(known_tickets.union(new_tickets))
    except Exception as e:
        logger.error(f"Ticket: {ticket.ticket_id} Error {e}.")
        await bot.send_message(chat_id=CHAT_ID, text=f"Ошибка с тикетом {ticket.ticket_id}", parse_mode=ParseMode.HTML)
        save_new_tickets(known_tickets.union(new_tickets))

async def polling():
    api = TicketsAPI()
    while True:
        tickets = api.get_open_tickets_info()
        known_tickets = load_known_tickets()
        sla_broken = []
        for ticket in tickets:
            sla = int(int(ticket.SLA_ends)/1000) - int(dt.now().timestamp())
            if sla == int(dt.now().timestamp()) * -1:
                pass
            elif sla < 0 and ticket.ticket_id not in known_tickets:
                sla_broken.append(ticket.ticket_id)
        
        
        if len(sla_broken) != 0:
            logger.info(f"{len(sla_broken)} tickets with broken SLA.")
            await mention_broken_SLA(sla_broken)
        else:
            logger.info(f"No new broken SLA.")
        time.sleep(600)

if __name__ == "__main__":
    asyncio.run(polling())