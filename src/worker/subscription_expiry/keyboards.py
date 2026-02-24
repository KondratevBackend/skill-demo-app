from aiogram import types
from aiogram.enums import ButtonStyle

sub_expiry_keyboard = types.InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="👉 Продлить подписку 👈",
                callback_data="start",
                style=ButtonStyle.SUCCESS,
            )
        ],
        [
            types.InlineKeyboardButton(text="Поддержка 🛠", callback_data="support")
        ],
    ]
)