from aiogram import Bot, Dispatcher

from src.bot.admin.coupon.handlers import CouponAdminHandlers
from src.bot.admin.start.handlers import StartAdminHandlers
from src.bot.coupon.handlers import CouponHandlers
from src.bot.start.handlers import StartHandlers
from src.bot.tariff.handlers import BotTariffHandlers


class RegisterHandlers:
    def __init__(
        self,
        start_handlers: StartHandlers,
        tariff_handlers: BotTariffHandlers,
        coupon_handlers: CouponHandlers,
        start_admin_handlers: StartAdminHandlers,
        coupon_admin_handlers: CouponAdminHandlers,
    ):
        self._start_handlers = start_handlers
        self._tariff_handlers = tariff_handlers
        self._coupon_handlers = coupon_handlers

        # admin
        self._start_admin_handlers = start_admin_handlers
        self._coupon_admin_handlers = coupon_admin_handlers

    def set(self, dp: Dispatcher, bot: Bot):
        self._start_handlers.register_handlers(dp)
        self._tariff_handlers.register_handlers(dp)
        self._coupon_handlers.register_handlers(dp)

        # admin
        self._start_admin_handlers.register_handlers(dp)
        self._coupon_admin_handlers.register_handlers(dp)
