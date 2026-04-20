import random

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from src.bot.start.dao import StartDAO
from src.bot.start.keyboards import StartKeyboard

START_AGAIN_MESSAGES = [
    "С возвращением! <tg-emoji emoji-id='5343984088493599366'>👋</tg-emoji>",
    "Рады видеть тебя снова <tg-emoji emoji-id='5325559344513691205'>😎</tg-emoji>",
    "Привет ещё раз <tg-emoji emoji-id='5363836475307730046'>😚</tg-emoji>",
    "С возвращением в YourApp <tg-emoji emoji-id='5188481279963715781'>🚀</tg-emoji>",
    "И снова ты — отличное решение <tg-emoji emoji-id='5388743385794228775'>😊</tg-emoji>",
    "С любовью YourApp <tg-emoji emoji-id='5397890811436213746'>🫶</tg-emoji>",
    "YourApp снова на связи <tg-emoji emoji-id='5397890811436213746'>🫶</tg-emoji>",
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
            message = await message.answer(
                "<tg-emoji emoji-id='5224607267797606837'>☄️</tg-emoji>",
                reply_markup=await self._keyboard.start_reply_keyboard(),
                parse_mode=ParseMode.HTML,
            )

        msg_text = (
            f"{random.choice(START_AGAIN_MESSAGES)}\n\n"
            f"<tg-emoji emoji-id='5456140674028019486'>⚡️</tg-emoji> Быстро.\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> Без ограничений.\n"
            f"<tg-emoji emoji-id='5197288647275071607'>🛡</tg-emoji> Без логов.\n\n"
            f"Выбирай тариф и подключайся за 1 минуту <tg-emoji emoji-id='5406745015365943482'>⬇️</tg-emoji>"
        )

        if not await self._dao.exists_user(telegram_id=message.from_user.id):
            msg_text = (
                f"<b>Добро пожаловать в YourApp!</b>\n\n"
                f"<tg-emoji emoji-id='5456140674028019486'>⚡️</tg-emoji> Быстро.\n"
                f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> Без ограничений.\n"
                f"<tg-emoji emoji-id='5197288647275071607'>🛡</tg-emoji> Без логов.\n\n"
                f"Выбирай тариф и подключайся за 1 минуту <tg-emoji emoji-id='5406745015365943482'>⬇️</tg-emoji>"
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
