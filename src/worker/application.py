import logging

from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisStreamBroker

from src.core.config import WorkerConfig

logger = logging.getLogger(__name__)


class WorkerApplication:
    def __init__(self, config: WorkerConfig):
        self._config = config
        self._broker = None
        self._scheduler = None

    @property
    def broker(self) -> RedisStreamBroker:
        if self._broker is not None:
            return self._broker

        _broker = RedisStreamBroker(url=self._config.broker.dsn.unicode_string())
        self._broker = _broker

        self._register_events(broker=_broker)

        return _broker

    @property
    def scheduler(self) -> TaskiqScheduler:
        if self._scheduler is not None:
            return self._scheduler

        _scheduler = TaskiqScheduler(
            broker=self.broker,
            sources=[LabelScheduleSource(self.broker)],
        )
        self._scheduler = _scheduler

        return _scheduler

    def _register_events(self, broker) -> None:
        @broker.on_event(TaskiqEvents.WORKER_STARTUP)
        async def startup(state: TaskiqState) -> None:
            logger.info("Worker startup")

        @broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
        async def shutdown(state: TaskiqState) -> None:
            logger.info("Worker shutdown")
