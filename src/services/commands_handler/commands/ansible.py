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
        sent_message = await message.answer(f"Обновление SupDemo:\nПрогресс:\n\n")
        await run_ansible_playbook(sent_message.chat.id, sent_message.message_id, sent_message.text)

    async def track_download_progress(chat_id, message_id, total_size, file_path):
        total_gb = total_size / (1024 ** 3)
        pass

    async def run_ansible_playbook(chat_id, message_id, original_text):
        path_to_playbook = os.path.join("/app", "ansible", "update.yml")
        path_to_hosts = os.path.join("/app", "ansible", "hosts.ini")
        
        result = await asyncio.create_subprocess_exec(
            "ansible-playbook", "-i", path_to_hosts, path_to_playbook,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        if result.returncode == 0:
            await BOT.edit_message_text(chat_id, message_id, text=original_text + "✅ Обновление успешно завершено!")
        else:
            await BOT.edit_message_text(chat_id, message_id, text=original_text + f"\n❌ Ошибка при обновлении:\n{stderr.decode()}")