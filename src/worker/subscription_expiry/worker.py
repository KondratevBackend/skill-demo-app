import logging

from taskiq import TaskiqDepends

from src.worker.main import container, broker
from src.worker.subscription_expiry.service import SubscriptionExpiryWorkerService


logger = logging.getLogger(__name__)


def get_service() -> SubscriptionExpiryWorkerService:
    return container.resolve(SubscriptionExpiryWorkerService)


@broker.task(schedule=[{"cron": "* * * * *"}])
async def tariff_expiry_worker(service: SubscriptionExpiryWorkerService = TaskiqDepends(get_service)):
    logger.debug("Subscription expiry job started")
    await service.process()
    logger.debug("Subscription expiry job completed")
