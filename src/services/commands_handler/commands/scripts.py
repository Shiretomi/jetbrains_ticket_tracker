from aiogram.filters import Command
from aiogram.types import Message
from common.utils import acl
from loguru import logger

import os, re

def init_scripts(bot):
    SCRIPTS_FOLDER = "./scripts"

    DESCRIPTION_PATTERN = re.compile(r'^#\s*Description:\s*(.*)$', re.IGNORECASE | re.MULTILINE)

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

            scripts_info.append(f"{script} - {description}")
        
        return scripts_info

    @bot.message(Command("get_scripts"), acl.isSupportTeam())
    async def get_scripts(message: Message):
        msg = "Для получения ссылки на скрипт, нажмите на название скрипта.\n\n"
        scripts = list_scripts()
        script_list = '\n'.join(scripts)
        await message.answer(f"{msg}{script_list}")