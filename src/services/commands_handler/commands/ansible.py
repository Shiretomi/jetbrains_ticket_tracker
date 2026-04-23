import asyncio
import os
import time

from common.utils import acl
from common.utils.config import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command 
from aiogram.types import Message
from aiogram import Bot, html, F, types

TOKEN = config['telegram_token']

BOT = Bot(TOKEN)

ERROR = "fatal: ["
CURRENT_HASH_TRIGGER = '"msg": "Current hash: '
NEW_HASH_TRIGGER = '"msg": "New hash: '

STEP_MAP = {
    "TASK [Find installer in repo.int.ntl": "🔍 Ищу инсталлятор в репозитории...",
    "TASK [Cleanup old": "🧹 Очищаю старые файлы, если остались...",
    "TASK [Download installer": "⚙️ Скачиваю инсталлер на сервер...",
    "TASK [Unzip installer": "📦 Вытаскиваю образы из инсталлера...",
    "TASK [Load multi": "🗄 Загружаю новые образы multi...",
    "TASK [Load universe": "🗄 Загружаю новые образы universe...",
    "TASK [Last cleanup": "🧹 Очищаю временные файлы...",
    "TASK [Restart ": "🐳 Перезапускаю контейнеры...",
}

def init_ansible(bot):
    async def confirm_kb():
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="Да",
            callback_data="update_supdemo"
        ))
        builder.add(InlineKeyboardButton(
            text="Нет",
            callback_data="cancel_supdemo"
        ))

        return builder.as_markup()

    @bot.callback_query(F.data == "update_supdemo", acl.isSupportTeam())
    async def update_supdemo(callback: types.CallbackQuery):
        await callback.message.delete()
        sent_message = await callback.message.answer(f"Обновление Sup_demo\n\n\
Прогресс:\
\n\n", parse_mode=ParseMode.HTML)
        
        await run_ansible_playbook(sent_message.chat.id, sent_message.message_id, sent_message.text)

    @bot.callback_query(F.data == "cancel_supdemo", acl.isSupportTeam())
    async def cancel_supdemo(callback: types.CallbackQuery):
        await callback.message.delete()

    @bot.message(Command("update_supdemo"), acl.isSupportTeam(), acl.isTimeToUpdate())
    async def update(message: Message):
        await message.answer("Хотите обновить Sup_demo?", reply_markup=await confirm_kb())
        

    async def run_ansible_playbook(chat_id, message_id, original_text):
        path_to_playbook = os.path.join("/app", "ansible", "update.yml")
        path_to_hosts = os.path.join("/app", "ansible", "hosts.ini")
        
        start_time = time.perf_counter()

        process = await asyncio.create_subprocess_exec(
            "ansible-playbook", "-i", path_to_hosts, path_to_playbook,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        text_to_edit = original_text
        current_status = "🔄 Начинаю обновление...\n"
        last_status = ""

        current_hash = ""
        new_hash = ""

        error_msg = ""

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
                if ERROR in decoded_line:
                    error_msg = decoded_line
                if CURRENT_HASH_TRIGGER in decoded_line:
                    current_hash = decoded_line.split(CURRENT_HASH_TRIGGER)[1][:-1]
                if NEW_HASH_TRIGGER in decoded_line:
                    new_hash = decoded_line.split(NEW_HASH_TRIGGER)[1][:-1]

        
            #обновление статуса бота
            if current_status != last_status:
                try:
                    match current_status:
                        case "🔄 Начинаю обновление...\n":
                            text_to_edit = f'{text_to_edit}\n\n{html.italic(current_status)}'
                        case "🔍 Ищу инсталлятор в репозитории...":
                            text_to_edit = f'{text_to_edit}\n{html.code(current_status)}'
                        case _:
                            text_to_edit = f'{text_to_edit} ✅\n{html.code(current_status)}'
                    
                    await BOT.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text_to_edit,
                        parse_mode=ParseMode.HTML
                    )
                    last_status = current_status
                except Exception as e:
                    pass
        _, stderr = await process.communicate()

        end_time = time.perf_counter()
        duration = int(end_time - start_time)
        minutes = duration // 60
        seconds = duration % 60
        time_str = f"{minutes} мин. {seconds} сек." if minutes > 0 else f"{seconds} сек."

        if process.returncode == 0:
            builds = f'{html.code(current_hash)} >> {html.code(new_hash)}'
            message = f'{text_to_edit} ✅\n\n✅ Обновление успешно завершено!\n\nВерсия билда\n{builds}\n\nОбновлено за\n{time_str}'
            
            await BOT.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode=ParseMode.HTML
                )
            await BOT.send_message(
                chat_id=chat_id,
                reply_to_message_id=message_id,
                text="✅ Обновление завершено успешно!",
                parse_mode=ParseMode.HTML
                )
        else:
            await BOT.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'{text_to_edit}❌\n\n❌ Ошибка при обновлении:\n{html.expandable_blockquote(error_msg)}',
                parse_mode=ParseMode.HTML
            )
            await BOT.send_message(
                chat_id=chat_id,
                reply_to_message_id=message_id,
                text="❌ Обновление завершено с ошибками",
                parse_mode=ParseMode.HTML
                )