from aiogram import Bot
from os import getenv
from dotenv import load_dotenv
from loguru import logger
from common.utils.tickets_api import TicketsAPI
from common.models.ticket import Ticket
from datetime import datetime as dt 

import asyncio
import time

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")
bot = Bot(TOKEN)

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
    known_tickets = load_known_tickets()
    new_tickets = []
    for ticket in tickets:
        if ticket in known_tickets:
            continue
        else:
            #TODO: пинг через конфиг ямл
            new_tickets.append(ticket)
            ticket = Ticket.from_youtrack(ticket)
            msg = f'''🔴Истек срок решения🔴\
                        \n{ticket.ticket_id}\
                        \n{ticket.name}\
                        \nhttps://tracker.ntechlab.com/tickets/{ticket.ticket_id}\
                        \n{ticket.assignee}
                        '''
            await bot.send_message(chat_id=CHAT_ID, text=msg)
    save_new_tickets(known_tickets.union(new_tickets))

async def polling():
    api = TicketsAPI()
    while True:
        tickets = api.get_open_tickets_info()
        sla_broken = []
        for ticket in tickets:
            sla = int(int(ticket.SLA_ends)/1000) - int(dt.now().timestamp())
            if sla == int(dt.now().timestamp()) * -1:
                pass
            elif sla < 0:
                sla_broken.append(ticket.ticket_id)
        
        
        if len(sla_broken) != 0:
            await mention_broken_SLA(sla_broken)

        time.sleep(600)

if __name__ == "__main__":
    asyncio.run(polling())