from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from common.utils import acl
from aiogram import html, F, Bot
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

class AddScript(StatesGroup):
    send_script = State()
    send_name = State()
    send_description = State()
    send_verify = State()

def init_scripts(bot):
    async def download_script_kb(script_name):
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text=f"Сгенерировать ссылку для удаленных хостов. (pastebin)",
            callback_data=f"download_script:{script_name}"
        ))

        return builder.as_markup()
    
    async def cancel_kb():
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel"
        ))

        return builder.as_markup()

    def insert_description(path: str, description: str) -> str:
        header = f"# Description: {description}\n"
        with open(path, 'r') as f:
            content = f.read()
        
        lines = content.splitlines()

        if lines and lines[0].startswith("#!"):
            lines.insert(1, header)
        else:
            lines.insert(0, header)
        
        rdy_content = "\n".join(lines)
        with open(path, 'w') as f:
            f.write(rdy_content)

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

    def write_script(script_name, code):
        path = os.path.join(SCRIPTS_FOLDER, script_name)
        with open(path, 'w') as f:
            f.write(code)

    @bot.message(Command("get_scripts"), acl.isSupportTeam())
    async def get_scripts(message: Message):
        msg = html.bold("Для получения скрипта, нажмите на название скрипта.\n\n")
        scripts = list_scripts()
        script_list = '\n'.join(scripts)
        await message.answer(f"{msg}{script_list}", parse_mode=ParseMode.HTML)

    @bot.message(CommandStart(deep_link=True), acl.isSupportTeam())
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

        try:
            msg = f"{html.bold(script_name)}\nДля прямого использования в терминале:\n"
            await message.answer(f"{msg}{html.pre(script_content)}", parse_mode=ParseMode.HTML, reply_markup=keyboard)
        except Exception as e:
            file = FSInputFile(path=path, filename=script_name)
            msg = f"{html.bold(script_name)}\nСкрипт большой, файл скрипта\n"
            await message.answer_document(caption=f"{msg}", parse_mode=ParseMode.HTML, reply_markup=keyboard, document=file)


    # ДОБАВЛЕНИЕ СКРИПТОВ    
    @bot.message(Command("add_script"), acl.isSupportTeam())
    async def add_script(message: Message, state: FSMContext):
        code_example = html.pre('#!/bin/bash\n\nsome_useful_code\n\necho \"something\"')
        await message.answer(f'{html.bold("Пришлите код в формате")}{code_example}\nЛибо файл со скриптом.', parse_mode=ParseMode.HTML, reply_markup=await cancel_kb())
        await state.set_state(AddScript.send_script)

    @bot.message(AddScript.send_script, acl.isSupportTeam(), F.text | F.document)
    async def add_script_step_one(message: Message, state: FSMContext):
        name_example = html.italic(f'Напишите название в формате {html.bold("example_name.sh")}')
        await message.answer(f"{html.bold('Как будет называться скрипт?')}\n{name_example}", parse_mode=ParseMode.HTML, reply_markup=await cancel_kb())
        if message.document:
            await state.update_data(script_type="file", file_id=message.document.file_id)
            await state.set_state(AddScript.send_name)
        elif message.text:
            await state.update_data(script_type="text", script_content=message.text)
            await state.set_state(AddScript.send_name)        

    @bot.message(AddScript.send_name, acl.isSupportTeam())
    async def add_script_step_two(message: Message, state: FSMContext):
        await message.answer(html.bold("Добавьте описание для скрипта."), parse_mode=ParseMode.HTML, reply_markup=await cancel_kb())
        await state.update_data(name=message.text)
        await state.set_state(AddScript.send_description)
      
    @bot.message(AddScript.send_description, acl.isSupportTeam())
    async def add_script_step_two(message: Message, state: FSMContext, bot: Bot):
        await state.update_data(description=message.text)
        final_data = await state.get_data()
        name = final_data.get("name")
        description = final_data.get("description")
        path = os.path.join(SCRIPTS_FOLDER, name)
        
        script_type = final_data.get("script_type")
        if script_type == "text":
            with open(path, 'w', encoding="utf-8", errors="ignore") as f:
                f.write(final_data.get("script_content"))

        if script_type == "file":
            file_id = final_data.get('file_id')
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, path)
        
        insert_description(path, description)

        await state.clear()
        await message.answer(f"Скрипт сохранен!\n{name} - {description}", parse_mode=ParseMode.HTML)