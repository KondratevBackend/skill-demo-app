from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_admin_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Создать купон", callback_data="admin_create_coupon"),
        ],
        [
            InlineKeyboardButton(text="Создать рекламодателя", callback_data="admin_create_lead"),
        ],
        [
            InlineKeyboardButton(text="Статистика рекламодателей", callback_data="admin_list_lead"),
        ],
    ],
)
