from aiogram import Bot, Dispatcher

from src.bot.admin.coupon.handlers import CouponAdminHandlers
from src.bot.admin.feedback.handlers import FeedbackAdminHandlers
from src.bot.admin.lead.handlers import LeadAdminHandlers
from src.bot.admin.start.handlers import StartAdminHandlers
from src.bot.coupon.handlers import CouponHandlers
from src.bot.lk.handlers import LKHandlers
from src.bot.start.handlers import StartHandlers
from src.bot.stop_fsm.handlers import StopFSMHandlers
from src.bot.tariff.handlers import BotTariffHandlers


class RegisterHandlers:
    def __init__(
        self,
        stop_fsm_handlers: StopFSMHandlers,
        start_handlers: StartHandlers,
        tariff_handlers: BotTariffHandlers,
        coupon_handlers: CouponHandlers,
        lk_handlers: LKHandlers,
        start_admin_handlers: StartAdminHandlers,
        coupon_admin_handlers: CouponAdminHandlers,
        lead_admin_handlers: LeadAdminHandlers,
        feedback_admin_handlers: FeedbackAdminHandlers,
    ):
        self._stop_fsm_handlers = stop_fsm_handlers
        self._start_handlers = start_handlers
        self._tariff_handlers = tariff_handlers
        self._coupon_handlers = coupon_handlers
        self._lk_handlers = lk_handlers

        # admin
        self._start_admin_handlers = start_admin_handlers
        self._coupon_admin_handlers = coupon_admin_handlers
        self._lead_admin_handlers = lead_admin_handlers
        self._feedback_admin_handlers = feedback_admin_handlers

    def set(self, dp: Dispatcher, bot: Bot):
        self._stop_fsm_handlers.register_handlers(dp)
        self._start_handlers.register_handlers(dp)
        self._tariff_handlers.register_handlers(dp)
        self._coupon_handlers.register_handlers(dp)
        self._lk_handlers.register_handlers(dp)

        # admin
        self._start_admin_handlers.register_handlers(dp)
        self._coupon_admin_handlers.register_handlers(dp)
        self._lead_admin_handlers.register_handlers(dp)
        self._feedback_admin_handlers.register_handlers(dp)
