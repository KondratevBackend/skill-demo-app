from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.start.dao import StartDAO


class StartService:
    def __init__(self, dao: StartDAO):
        self._dao = dao

    async def start(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()

        await message.answer("Привет 👋👋👋")
