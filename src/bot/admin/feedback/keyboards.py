from aiogram import types

create_feedback_skip_keyboard = types.InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Пропустить", callback_data="admin_create_feedback_skip")],
    ],
)

is_verified_user_in_feedback_keyboard = types.InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Да", callback_data="admin_create_feedback_verified_user:true")],
        [types.InlineKeyboardButton(text="Нет", callback_data="admin_create_feedback_verified_user:false")],
    ],
)
