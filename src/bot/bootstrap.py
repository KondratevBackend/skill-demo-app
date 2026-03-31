import punq

from src.bot.admin.coupon.dao import CouponAdminDAO
from src.bot.admin.coupon.handlers import CouponAdminHandlers
from src.bot.admin.coupon.keyboards import CouponAdminKeyboards
from src.bot.admin.coupon.service import CouponAdminService
from src.bot.admin.feedback.dao import FeedbackAdminDAO
from src.bot.admin.feedback.handlers import FeedbackAdminHandlers
from src.bot.admin.feedback.service import FeedbackAdminService
from src.bot.admin.filters import IsAdminFilter
from src.bot.admin.lead.dao import LeadAdminDAO
from src.bot.admin.lead.handlers import LeadAdminHandlers
from src.bot.admin.lead.keyboards import LeadAdminKeyboard
from src.bot.admin.lead.service import LeadAdminService
from src.bot.admin.start.handlers import StartAdminHandlers
from src.bot.admin.start.service import StartAdminService
from src.bot.coupon.dao import CouponDAO
from src.bot.coupon.handlers import CouponHandlers
from src.bot.coupon.service import CouponService
from src.bot.lk.dao import LKDAO
from src.bot.lk.handlers import LKHandlers
from src.bot.lk.service import LKService
from src.bot.middlewares import GlobalMiddleware
from src.bot.register_handlers import RegisterHandlers
from src.bot.start.dao import StartDAO
from src.bot.start.handlers import StartHandlers
from src.bot.start.keyboards import StartKeyboard
from src.bot.start.service import StartService
from src.bot.stop_fsm.handlers import StopFSMHandlers
from src.bot.stop_fsm.service import StopFSMService
from src.bot.subscription.dao import SubscriptionDAO
from src.bot.subscription.service import SubscriptionService
from src.bot.support.keyboards import SupportKeyboards
from src.bot.tariff.dao import BotTariffDAO
from src.bot.tariff.handlers import BotTariffHandlers
from src.bot.tariff.service import BotTariffService
from src.core.config import BotConfig as Config
from src.core.database import Database
from src.core.payment.dao import PaymentDAO
from src.core.payment.service import PaymentService
from src.core.payment.yookassa.api import YookassaAPI
from src.core.server.cookie.dao import ServerCookieDAO
from src.core.server.cookie.service import ServerCookieService
from src.core.server.dao import ServerDAO
from src.core.server.service import ServerService
from src.core.tariff.dao import TariffDAO
from src.core.tariff.service import TariffService


def resolve_resources(config: Config) -> punq.Container:
    container = punq.Container()

    container.register(
        service=Database,
        factory=Database,
        scope=punq.Scope.singleton,
        config=config.database,
    )
    container.register(
        service=GlobalMiddleware,
        factory=GlobalMiddleware,
        scope=punq.Scope.singleton,
        config=config,
    )
    container.register(
        service=ServerCookieService,
        factory=ServerCookieService,
        scope=punq.Scope.singleton,
        config=config.server,
    )
    container.register(
        service=ServerCookieDAO,
        factory=ServerCookieDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=RegisterHandlers,
        factory=RegisterHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StopFSMHandlers,
        factory=StopFSMHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StopFSMService,
        factory=StopFSMService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=ServerService,
        factory=ServerService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=ServerDAO,
        factory=ServerDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=TariffDAO,
        factory=TariffDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=TariffService,
        factory=TariffService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=SubscriptionService,
        factory=SubscriptionService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=SubscriptionDAO,
        factory=SubscriptionDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponHandlers,
        factory=CouponHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponService,
        factory=CouponService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponDAO,
        factory=CouponDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=SupportKeyboards,
        factory=SupportKeyboards,
        scope=punq.Scope.singleton,
        config=config,
    )
    container.register(
        service=LKHandlers,
        factory=LKHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=LKService,
        factory=LKService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=LKDAO,
        factory=LKDAO,
        scope=punq.Scope.singleton,
    )

    register_admin(container=container, config=config)
    register_start(container=container)
    register_bot_tariff(container=container)
    register_payment(container=container, config=config)

    return container


def register_admin(container: punq.Container, config: Config) -> None:
    container.register(
        service=IsAdminFilter,
        factory=IsAdminFilter,
        scope=punq.Scope.singleton,
        config=config,
    )
    container.register(
        service=StartAdminHandlers,
        factory=StartAdminHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartAdminService,
        factory=StartAdminService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponAdminHandlers,
        factory=CouponAdminHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponAdminService,
        factory=CouponAdminService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponAdminDAO,
        factory=CouponAdminDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=CouponAdminKeyboards,
        factory=CouponAdminKeyboards,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=LeadAdminHandlers,
        factory=LeadAdminHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=LeadAdminService,
        factory=LeadAdminService,
        scope=punq.Scope.singleton,
        config=config,
    )
    container.register(
        service=LeadAdminDAO,
        factory=LeadAdminDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=LeadAdminKeyboard,
        factory=LeadAdminKeyboard,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=FeedbackAdminDAO,
        factory=FeedbackAdminDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=FeedbackAdminService,
        factory=FeedbackAdminService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=FeedbackAdminHandlers,
        factory=FeedbackAdminHandlers,
        scope=punq.Scope.singleton,
    )


def register_start(container: punq.Container) -> None:
    container.register(
        service=StartHandlers,
        factory=StartHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartService,
        factory=StartService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartDAO,
        factory=StartDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=StartKeyboard,
        factory=StartKeyboard,
        scope=punq.Scope.singleton,
    )


def register_bot_tariff(container: punq.Container) -> None:
    container.register(
        service=BotTariffHandlers,
        factory=BotTariffHandlers,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=BotTariffService,
        factory=BotTariffService,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=BotTariffDAO,
        factory=BotTariffDAO,
        scope=punq.Scope.singleton,
    )


def register_payment(container: punq.Container, config: Config) -> None:
    container.register(
        service=PaymentService,
        factory=PaymentService,
        scope=punq.Scope.singleton,
        config=config.yookassa,
    )
    container.register(
        service=PaymentDAO,
        factory=PaymentDAO,
        scope=punq.Scope.singleton,
    )
    container.register(
        service=YookassaAPI,
        factory=YookassaAPI,
        scope=punq.Scope.singleton,
        config=config.yookassa,
    )
