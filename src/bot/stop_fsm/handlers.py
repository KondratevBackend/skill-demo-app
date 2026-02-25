from aiogram import Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.stop_fsm.service import StopFSMService


class StopFSMHandlers:
    def __init__(self, service: StopFSMService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.message(Command("stop"))
        @dp.message(F.text.lower().in_(["stop", "стоп"]))
        async def stop_fsm_handler(message: types.Message, state: FSMContext):
            await self._service.stop_fsm(message=message, state=state)

        @dp.callback_query(F.data == "stop")
        async def stop_fsm_callback_handler(callback: types.CallbackQuery, state: FSMContext):
            await callback.answer("Останавливаем действие")
            await self._service.stop_fsm(message=callback.message, state=state)
