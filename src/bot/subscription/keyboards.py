from aiogram import types

instruction_keyboard = types.InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[[types.InlineKeyboardButton(text="Инструкция 🗂", callback_data="instruction")]]
)
