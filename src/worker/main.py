import punq
from taskiq import TaskiqScheduler
from taskiq_redis import RedisStreamBroker

from src.core.config import WorkerConfig
from src.worker.application import WorkerApplication
from src.worker.bootstrap import resolve_resources

config = WorkerConfig()
container: punq.Container = resolve_resources(config=config)
container.register(service=WorkerApplication, factory=WorkerApplication, scope=punq.Scope.singleton, config=config)
application: WorkerApplication = container.resolve(service_key=WorkerApplication)
broker: RedisStreamBroker = application.broker
scheduler: TaskiqScheduler = application.scheduler
