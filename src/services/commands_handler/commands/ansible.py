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

STEP_MAP = {
    "TASK [Find installer in repo.int.ntl": "🔍 Ищу инсталлятор в репозитории...",
    "TASK [Extract installer name": "🔍 Ищу имя инсталлятора...",
    "TASK [Run installation": "⚙️ Устанавливаю пакет на сервер...",
    "TASK [Cleanup": "🧹 Очищаю временные файлы..."
}

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
        
        process = await asyncio.create_subprocess_exec(
            "ansible-playbook", "-i", path_to_hosts, path_to_playbook,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        text_to_edit = original_text
        current_status = "Начинаю обновление...\n"
        last_status = ""

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode().strip()
            print(decoded_line)

            for trigger, status_text in STEP_MAP.items():
                if trigger in decoded_line:
                    current_status = status_text
                    break
        
            if current_status != last_status:
                try:
                    text_to_edit = f'{text_to_edit}✅\n{current_status}' if "Начинаю обновление..." not in current_status and "Прогресс:" not in current_status else f'{text_to_edit}\n'
                    await BOT.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text_to_edit
                    )
                    last_status = current_status
                except Exception as e:
                    pass
        _, stderr = await process.communicate()

        if process.returncode == 0:
            await BOT.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'{text_to_edit}✅\n\n✅ Обновление успешно завершено!'
                )
        else:
            await BOT.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'{text_to_edit}❌\n\n❌ Ошибка при обновлении:\n{stderr.decode()[-500:]}',
                parse_mode="Markdown"
                )