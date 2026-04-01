from aiogram import types

feedback_keyboard = types.InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Следующий отзыв",
                callback_data="feedback_next",
                icon_custom_emoji_id="5416117059207572332",
            ),
        ]
    ]
)