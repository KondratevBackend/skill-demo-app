from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot.coupon.dao import CouponDAO
from src.bot.coupon.fsm import CouponFSM


class CouponService:
    def __init__(self, dao: CouponDAO):
        self._dao = dao

    async def start_coupon(self, callback: types.CallbackQuery, state: FSMContext):
        await state.set_state(CouponFSM.get_code)
        await callback.message.edit_text(
            "🎟️ Напиши код купона: ",
            parse_mode="html",
        )

    async def activate_coupon(self, message: types.Message, state: FSMContext):
        pass
