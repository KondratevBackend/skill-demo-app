from aiogram import Dispatcher, F, types

from src.bot.admin.coupon.service import CouponAdminService
from src.bot.admin.filters import IsAdminFilter


class CouponAdminHandlers:
    def __init__(self, service: CouponAdminService, is_admin_filter: IsAdminFilter):
        self._service = service
        self._is_admin_filter = is_admin_filter

    def register_handlers(self, dp: Dispatcher):
        @dp.callback_query(self._is_admin_filter, F.data == "admin_create_coupon")
        async def start_coupon_handler(callback: types.CallbackQuery):
            await self._service.get_tariffs(callback=callback)

        @dp.callback_query(self._is_admin_filter, F.data.startswith("admin_create_coupon:"))
        async def start_coupon_handler(callback: types.CallbackQuery):
            await self._service.create_coupon(callback=callback)

