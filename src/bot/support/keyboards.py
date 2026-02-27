from aiogram import types

from src.core.config import BotConfig
from src.core.consts import SUPPORT_BUTTON_TEXT


class SupportKeyboards:
    def __init__(self, config: BotConfig):
        self._config = config

    def common_problems_keyboard(self):
        # TODO: If support is overloaded with similar questions, then they can be implemented here
        pass

    @property
    def support_button(self):
        return types.InlineKeyboardButton(text=SUPPORT_BUTTON_TEXT, url=self._config.bot.support_url)

    def support_keyboard(self):
        return types.InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[[self.support_button]],
        )
