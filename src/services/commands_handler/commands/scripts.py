from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.types import Message
from common.utils import acl
from aiogram import html
from loguru import logger
from os import getenv
from dotenv import load_dotenv

import requests
import os, re

load_dotenv()

SCRIPTS_FOLDER = "./scripts"
    
BOT_NAME = requests.get(f"https://api.telegram.org/bot{getenv('TELEGRAM_TOKEN')}/getMe").json()['result']['username']

DESCRIPTION_PATTERN = re.compile(r'^#\s*Description:\s*(.*)$', re.IGNORECASE | re.MULTILINE)

SEPARATOR = "_bot-tech-separator_"

def init_scripts(bot):
    async def download_script_kb(script_name):
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text=f"Сгенерировать ссылку для удаленных хостов. (pastebin)",
            callback_data=f"download_script:{script_name}"
        ))

        return builder.as_markup()


    def list_scripts():
        scripts_info = []
        for script in os.listdir(SCRIPTS_FOLDER):
            path = os.path.join(SCRIPTS_FOLDER, script)
            description = "Описание отсутствует"

            try:
                with open(path, 'r', encoding="utf-8", errors="ignore") as f:
                    head = []
                    for _ in range(10):
                        line = f.readline()
                        if not line: break
                        head.append(line)

                    content_head = "".join(head)
                    found_description = DESCRIPTION_PATTERN.search(content_head)

                    if found_description:
                        description = found_description.group(1).strip()
            
            except Exception as e:
                logger.error(type(e).__name__)

            payload = script.replace('.', SEPARATOR)
            link = f"https://t.me/{BOT_NAME}?start={payload}"

            scripts_info.append(f"{html.link(script, link)} - {html.italic(description)}")
        
        return scripts_info

    @bot.message(Command("get_scripts"), acl.isSupportTeam())
    async def get_scripts(message: Message):
        msg = html.bold("Для получения скрипта, нажмите на название скрипта.\n\n")
        scripts = list_scripts()
        script_list = '\n'.join(scripts)
        await message.answer(f"{msg}{script_list}", parse_mode=ParseMode.HTML)

    @bot.message(CommandStart(deep_link=True))
    async def send_script(message: Message, command: CommandObject):
        keyboard = await download_script_kb(command.args)
        script_name = command.args.replace(SEPARATOR, ".")
        path = os.path.join(SCRIPTS_FOLDER, script_name)
        script_content = "Ошибка чтения"
        try:
            with open(path, 'r', encoding="utf-8", errors="ignore") as f:
                script_content = f.read()
        except Exception as e:
            pass

        msg = f"{html.bold(script_name)}\nДля прямого использования в терминале:\n"
        await message.answer(f"{msg}{html.pre(script_content)}", parse_mode=ParseMode.HTML, reply_markup=keyboard)