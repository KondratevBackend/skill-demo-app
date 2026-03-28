import random

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.start.dao import StartDAO
from src.bot.start.keyboards import StartKeyboard

START_AGAIN_MESSAGES = [
    "С возвращением! 👋",
    "Рады видеть тебя снова 😎",
    "Привет ещё раз 😉",
    "С возвращением в Приватка VPN 🚀",
    "И снова ты — отличное решение 😌",
    "С любовью Приватка ❤️",
    "Приватка VPN снова на связи 💜",
]


class StartService:
    def __init__(self, dao: StartDAO, keyboard: StartKeyboard):
        self._dao = dao
        self._keyboard = keyboard

    async def start(self, message: types.Message, state: FSMContext, with_smile: bool = True):
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()

        if with_smile:
            await message.answer(
                "✨",
                reply_markup=await self._keyboard.start_reply_keyboard(),
            )

        msg_text = (
            f"{random.choice(START_AGAIN_MESSAGES)}\n\n"
            f"⚡️ Быстро.\n"
            f"🌍 Без ограничений.\n"
            f"🛡 Без логов.\n\n"
            f"Выбирай тариф и подключайся за 1 минуту 👇"
        )

        if not await self._dao.exists_user(telegram_id=message.from_user.id):
            msg_text = (
                f"<b>Добро пожаловать в Приватка VPN!</b>\n\n"
                f"⚡️ Быстро.\n"
                f"🌍 Без ограничений.\n"
                f"🛡 Без логов.\n\n"
                f"Выбирай тариф и подключайся за 1 минуту 👇"
            )
            user = await self._dao.create_user(telegram_user=message.from_user)

            start_parameter: str = message.text.split(" ")[-1]
            if start_parameter.isdigit():
                await self._referral_registration(user_id=user.id, referral_id=start_parameter)
            elif start_parameter.isascii() and start_parameter.isalpha():
                await self._lead_user_registration(user_id=user.id, lead_url_code=start_parameter)

        await message.answer(
            text=msg_text,
            parse_mode="html",
            reply_markup=await self._keyboard.start_inline_keyboard(),
        )

    async def _referral_registration(self, user_id: int, referral_id: int) -> None:
        pass

    async def _lead_user_registration(self, user_id: int, lead_url_code: str) -> None:
        # TODO: Errors handler
        lead_id = await self._dao.get_lead_id_by_url_code(url_code=lead_url_code)
        exists_lead_user = await self._dao.exists_lead_user(user_id=user_id, lead_id=lead_id)
        if not exists_lead_user:
            await self._dao.create_lead_user(user_id=user_id, lead_id=lead_id)
