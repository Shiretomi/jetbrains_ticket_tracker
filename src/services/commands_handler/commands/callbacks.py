import requests, os

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram import types
from common.utils import tickets_api
from common.utils import uploads, acl
from aiogram import Bot, html
from aiogram.enums import ParseMode

API = tickets_api.TicketsAPI()

SEPARATOR = "_bot-tech-separator_"

SCRIPTS_FOLDER = "./scripts"

class Select(StatesGroup):
    next_option = State()

async def spam_button(ticket_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Спам",
        callback_data=f"spam_ticket:{ticket_id}"
    ))
    return builder.as_markup()

async def kb_sumbit():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Вы точно хотите отправить тикет в спам?\n(Да)",
        callback_data='spam_yes'
    ))
    builder.row(InlineKeyboardButton(
        text="Нет",
        callback_data="spam_no"
    ))
    return builder.as_markup()

def init_callbacks(bot):
    @bot.callback_query(F.data.startswith('spam_ticket'))
    async def spam_button_callback(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=await kb_sumbit())
        await state.update_data(ticket_id = callback.data.split(":")[1])
        await state.set_state(Select.next_option)

    @bot.callback_query(Select.next_option, F.data == "spam_yes")
    async def spam_yes(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        ticket_id = data.get("ticket_id")
        API.send_to_spam(ticket_id)

        msg = f"Тикет {ticket_id} отправлен в спам"

        await state.clear()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=None)
        await callback.bot.send_message(chat_id=callback.from_user.id, text=msg)
        
    @bot.callback_query(Select.next_option, F.data == "spam_no")
    async def spam_no(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=await spam_button(data.get("ticket_id")))
        await state.clear()

    @bot.callback_query(F.data.startswith('download_script'), acl.isSupportTeam())
    async def generate_link(callback: types.CallbackQuery):
        script_name = callback.data.split(":")[1].replace(SEPARATOR, '.')
        path = os.path.join(SCRIPTS_FOLDER, script_name)

        try:
            with open(path, 'r', encoding="utf-8", errors="ignore") as f:
                script_content = f.read()
        except Exception as e:
            pass

        link = await uploads.upload_to_pastebin(script_name, script_content)
        if link and link.startswith("https"):
            link = link.replace("pastebin.com/", "pastebin.com/raw/")
            msg = html.bold("Ссылка для скачивания и запуска:\n")
            command = f"curl -sSL {link} | bash"
            await callback.message.answer(f"{msg}{html.pre(command)}", reply_to_message_id=callback.message.message_id, parse_mode=ParseMode.HTML)
        else:
            await callback.message.answer("❌ Ошибка при загрузке на Pastebin.")

    @bot.callback_query(F.data == "cancel")
    async def cancel(callback: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.answer("Операция отменена")