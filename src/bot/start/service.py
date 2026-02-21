from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.start.dao import StartDAO
from src.bot.start.keyboards import StartKeyboard


class StartService:
    def __init__(self, dao: StartDAO, keyboard: StartKeyboard):
        self._dao = dao
        self._keyboard = keyboard

    async def start(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()

        if not await self._dao.exists_user(telegram_id=message.from_user.id):
            await self._dao.create_user(telegram_user=message.from_user)

        await message.answer(
            "✨",
            reply_markup=await self._keyboard.start_reply_keyboard(),
        )
        await message.answer(
            f"<b>Добро пожаловать в Приватка VPN!</b>\n\n"
            f"⚡️ Быстро.\n"
            f"🌍 Без ограничений.\n"
            f"🛡 Без логов.\n\n"
            f"Выбирай тариф и подключайся за 1 минуту 👇",
            parse_mode="html",
            reply_markup=await self._keyboard.start_inline_keyboard(),
        )
