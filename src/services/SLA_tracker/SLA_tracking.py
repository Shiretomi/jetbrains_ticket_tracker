from aiogram import Bot
from os import getenv
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")
bot = Bot(TOKEN)

