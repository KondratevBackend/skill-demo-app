from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

stop_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Остановить 🟥", callback_data="stop"),
        ]
    ],
)
