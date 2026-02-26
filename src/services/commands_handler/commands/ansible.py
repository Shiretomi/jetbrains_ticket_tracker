import asyncio
import os

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
    "TASK [Download installer": "⚙️ Скачиваю инсталлер на сервер...",
    "TASK [Unzip installer": "📦 Вытаскиваю образы из инсталлера...",
    "TASK [Cleanup": "🧹 Очищаю временные файлы..."
}

def init_ansible(bot):
    @bot.message(Command("update_supdemo"))
    async def update(message: Message):
        sent_message = await message.answer(f"Обновление SupDemo\nПрогресс:\n\n")
        await run_ansible_playbook(sent_message.chat.id, sent_message.message_id, sent_message.text)

    async def run_ansible_playbook(chat_id, message_id, original_text):
        path_to_playbook = os.path.join("/app", "ansible", "update.yml")
        path_to_hosts = os.path.join("/app", "ansible", "hosts.ini")
        
        process = await asyncio.create_subprocess_exec(
            "ansible-playbook", "-i", path_to_hosts, path_to_playbook,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        text_to_edit = original_text
        current_status = "🔄 Начинаю обновление...\n"
        last_status = ""

        while True:
            #чтение stdout
            line = await process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode().strip()
            print(decoded_line)

            #вычленение триггер слов для бота
            for trigger, status_text in STEP_MAP.items():
                if trigger in decoded_line:
                    current_status = status_text
                    break
        
            #обновление статуса бота
            if current_status != last_status:
                try:
                    match current_status:
                        case "🔄 Начинаю обновление...\n":
                            text_to_edit = f'{text_to_edit}\n\n{current_status}'
                        case "🔍 Ищу инсталлятор в репозитории...":
                            text_to_edit = f'{text_to_edit}\n{current_status}'
                        case _:
                            text_to_edit = f'{text_to_edit} ✅\n{current_status}'
                    
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
                text=f'{text_to_edit} ✅\n\n ✅Обновление успешно завершено!'
                )
        else:
            await BOT.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'{text_to_edit}❌\n\n❌ Ошибка при обновлении:\n{stderr.decode()[-500:]}',
                parse_mode="Markdown"
            )