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
        try:
            result = subprocess.run(
                ["ansible-playbook", "-i", path_to_hosts, path_to_playbook],
                capture_output=True,
                text=True,
                check=True
            )
            await BOT.send_message(chat_id, f"Ansible playbook executed successfully:\n{result.stdout}", reply_to_message_id=message_id)
        except subprocess.CalledProcessError as e:
            await BOT.send_message(chat_id, f"Error running Ansible playbook: {e}", reply_to_message_id=message_id)