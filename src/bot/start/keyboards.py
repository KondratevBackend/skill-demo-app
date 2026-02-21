from aiogram import types
from aiogram.enums import ButtonStyle

from src.bot.start.dao import StartDAO


class StartKeyboard:
    def __init__(self, dao: StartDAO):
        self._dao = dao

    async def start_keyboard(self) -> types.InlineKeyboardMarkup:
        tariffs = await self._dao.get_tariffs()

        inline_keyboard: list = []
        for tariff in tariffs:
            style = None
            if not tariff.price:
                style = ButtonStyle.DANGER

            inline_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text=tariff.text,
                        callback_data=f"tariff_select_{tariff.id}",
                        style=style,
                    )
                ]
            )

        return types.InlineKeyboardMarkup(row_width=1, inline_keyboard=inline_keyboard)
