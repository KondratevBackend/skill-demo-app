from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.start.service import StartService


class StopFSMService:
    def __init__(self, start_service: StartService):
        self._start_service = start_service

    async def stop_fsm(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            await message.answer("Нечего останавливать 🙂")
            return
        await state.clear()
        await message.answer("Действие отменено")
        await self._start_service.start(message=message, state=state, with_smile=False)
