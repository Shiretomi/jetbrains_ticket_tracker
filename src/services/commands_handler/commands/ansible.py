import asyncio
import os
import subprocess

from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")

BOT = Bot(TOKEN)

def init_ansible(bot):
    @bot.message(Command("update_supdemo"))
    async def update(message: Message):
        await message.answer(f"Обновление SupDemo:\n\nDEBUG: {await run_ansible_playbook(message.chat.id, message.message_id)}")


    async def track_download_progress(chat_id, message_id, total_size, file_path):
        total_gb = total_size / (1024 ** 3)
        pass

    async def run_ansible_playbook(chat_id, message_id):
        path_to_playbook = os.path.join("/app", "ansible", "update.yml")
        path_to_hosts = os.path.join("/app", "ansible", "hosts.ini")
        
        result = await asyncio.create_subprocess_exec(
            "ansible-playbook", "-i", path_to_hosts, path_to_playbook,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        if result.returncode == 0:
            await BOT.send_message(chat_id, "✅ Обновление успешно завершено!")
        else:
            await BOT.send_message(chat_id, f"❌ Ошибка:\n{stderr.decode()}")