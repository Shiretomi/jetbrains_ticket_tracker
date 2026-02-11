import requests

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram import types
from common.utils import tickets_api
from aiogram import Bot


API = tickets_api.TicketsAPI()

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
        API.send_to_spam(data.get("ticket_id"))

        msg = f"Тикет {data.get("ticket_id")} отправлен в спам"

        await state.clear()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=None)
        await callback.bot.send_message(chat_id=callback.from_user.id, text=msg)
        
    @bot.callback_query(Select.next_option, F.data == "spam_no")
    async def spam_no(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=await spam_button(data.get("ticket_id")))
        await state.clear()