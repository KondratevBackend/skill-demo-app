from aiogram import Dispatcher, F, types

from src.bot.lk.service import LKService
from src.core.consts import LK_BUTTON_TEXT


class LKHandlers:
    def __init__(self, service: LKService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.message(
            F.text.in_(
                [
                    LK_BUTTON_TEXT,
                ]
            )
        )
        async def get_lk_handler(message: types.Message):
            await self._service.get_lk(message=message)
