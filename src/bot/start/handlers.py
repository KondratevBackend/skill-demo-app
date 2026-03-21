from aiogram import Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.start.service import StartService


class StartHandlers:
    def __init__(self, service: StartService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.message(Command("start"))
        async def start_handler(message: types.Message, state: FSMContext):
            await self._service.start(message=message, state=state)

        @dp.callback_query(F.data == "start")
        async def start_callback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer()
            await callback.message.delete()
            await self._service.start(message=callback.message, state=state)
