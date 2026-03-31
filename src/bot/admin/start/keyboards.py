from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.core import consts

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
            InlineKeyboardButton(
                text="Список рекламодателей",
                callback_data=f"admin_list_leads_{consts.PAGINATION_LIMIT_ADMIN_LIST_LEADS}:{consts.PAGINATION_OFFSET_ADMIN_LIST_LEADS}",
            ),
        ],
        [
          InlineKeyboardButton(text="Создать отзыв",callback_data="admin_create_feedback")
        ],
    ],
)
