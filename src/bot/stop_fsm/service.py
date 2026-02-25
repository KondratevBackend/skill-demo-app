from aiogram import types
from aiogram.fsm.context import FSMContext


class StopFSMService:
    async def stop_fsm(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            await message.answer("Нечего останавливать 🙂")
            return
        await state.clear()
        await message.answer("Действие отменено")
