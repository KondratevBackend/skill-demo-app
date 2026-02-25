from aiogram import Dispatcher, types
from aiogram.filters import Command

from src.bot.admin.filters import IsAdminFilter
from src.bot.admin.start.services import StartAdminService


class StartAdminHandlers:
    def __init__(self, service: StartAdminService, is_admin_filter: IsAdminFilter):
        self._service = service
        self._is_admin_filter = is_admin_filter

    def register_handlers(self, dp: Dispatcher):
        @dp.message(self._is_admin_filter, Command("admin"))
        async def start_handler(message: types.Message):
            await self._service.start(message=message)
