import random

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.coupon.dao import CouponDAO
from src.bot.coupon.fsm import CouponFSM
from src.bot.support.keyboards import SupportKeyboards
from src.core.tariff.service import TariffService


NOT_FOUND_COUPON_MESSAGES = [
    "❌ Купон не найден",
    "Не нашёл такой купон 👀\nВозможно, опечатка?",
    "Хмм… такого купона нет 🤔",
]


class CouponService:
    def __init__(
        self,
        dao: CouponDAO,
        tariff_service: TariffService,
        support_keyboards: SupportKeyboards,
    ):
        self._dao = dao
        self._tariff_service = tariff_service
        self._support_keyboards = support_keyboards

    async def start_coupon(self, callback: types.CallbackQuery, state: FSMContext):
        await state.set_state(CouponFSM.get_code)
        await callback.message.edit_text(
            "🎟️ <b>Напиши код купона:</b> ",
            parse_mode="html",
        )

    async def activate_coupon(self, message: types.Message, state: FSMContext):
        try:
            coupon_code: str = message.text

            coupon = await self._dao.get_coupon(code=coupon_code)
            if not coupon:
                await message.answer(
                    f"{random.choice(NOT_FOUND_COUPON_MESSAGES)}\n\n"
                    f"<b>Введи код ещё раз:</b>",
                    parse_mode="html",
                )
                return

            await state.clear()
            await self._dao.delete_coupon(coupon_id=coupon.id)
            user = await self._dao.get_user(telegram_id=message.from_user.id)
            await self._tariff_service.issue_tariff(user=user, tariff=coupon.tariff)
            await message.answer(
                f"✅ <b>Купон успешно активирован!</b>\n\n"
                f"Тебе начислено <i>{coupon.tariff.days} дней</i> безлимитного VPN 🚀\n\n"
                f"Пользуйся безопасно и без ограничений 💙",
                parse_mode="html",
                # TODO: keyboard lk
            )
        except Exception as e:
            await message.answer(
                "⚠️ Возникла техническая ошибка\n\n"
                "Пожалуйста, напиши в поддержку — мы разберёмся 👨‍🔧",
                parse_mode="html",
                reply_markup=self._support_keyboards.support_keyboard()
            )
            raise e
