from aiogram import Dispatcher, F, types
from aiogram.fsm.context import FSMContext

from src.bot.coupon.fsm import CouponFSM
from src.bot.coupon.service import CouponService


class CouponHandlers:
    def __init__(self, service: CouponService):
        self._service = service

    def register_handlers(self, dp: Dispatcher):
        @dp.callback_query(F.data == "coupon")
        async def start_coupon_handler(callback: types.CallbackQuery, state: FSMContext):
            await self._service.start_coupon(callback=callback, state=state)

        @dp.message(CouponFSM.get_code)
        async def activate_coupon_handler(message: types.Message, state: FSMContext):
            await self._service.activate_coupon(message=message, state=state)
