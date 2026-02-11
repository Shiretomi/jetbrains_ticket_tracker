from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

async def spam_button(ticket_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Спам",
        callback_data=f"spam_ticket:{ticket_id}"
    ))

    return builder.as_markup()