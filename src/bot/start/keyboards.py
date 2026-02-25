from aiogram import types
from aiogram.enums import ButtonStyle

from src.bot.start.dao import StartDAO
from src.core.consts import FEEDBACK_BUTTON_TEXT, LK_BUTTON_TEXT, REFERRAL_BUTTON_TEXT, SUPPORT_BUTTON_TEXT


class StartKeyboard:
    def __init__(self, dao: StartDAO):
        self._dao = dao

    @staticmethod
    async def start_reply_keyboard() -> types.ReplyKeyboardMarkup:
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text=LK_BUTTON_TEXT),
                    types.KeyboardButton(text=SUPPORT_BUTTON_TEXT),
                ],
                [
                    types.KeyboardButton(text=REFERRAL_BUTTON_TEXT),
                ],
                [
                    types.KeyboardButton(text=FEEDBACK_BUTTON_TEXT),
                ],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    async def start_inline_keyboard(self) -> types.InlineKeyboardMarkup:
        tariffs = await self._dao.get_tariffs()

        inline_keyboard: list = []
        for tariff in tariffs:
            style = None
            callback_data = f"tariff_select_{tariff.id}"
            if tariff.is_trial:
                style = ButtonStyle.DANGER
                callback_data = f"trial_tariff_select_{tariff.id}"

            inline_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text=tariff.text,
                        callback_data=callback_data,
                        style=style,
                    )
                ]
            )

        inline_keyboard.append([types.InlineKeyboardButton(text="Активировать купон",callback_data="coupon")])

        return types.InlineKeyboardMarkup(row_width=1, inline_keyboard=inline_keyboard)
