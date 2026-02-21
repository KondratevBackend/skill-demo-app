import datetime
from enum import StrEnum

from sqlalchemy import orm, DateTime, Enum, Integer, ForeignKey

from src.core.database import Base, mixins


class SubscriptionStatusType(StrEnum):
    active = "active"
    expired = "expired"
    canceled = "canceled"
    pending = "pending"


class Subscription(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    status: orm.Mapped[SubscriptionStatusType] = orm.mapped_column(Enum(SubscriptionStatusType), nullable=False)
    starts_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime, nullable=False)
    expires_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime, nullable=False)

    tariff_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("tariff.id"), nullable=False)
    user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    tariff = orm.relationship(
        "Tariff",
        back_populates="subscriptions",
        foreign_keys=[tariff_id],
        lazy="raise_on_sql",
    )
    user = orm.relationship(
        "User",
        back_populates="subscriptions",
        foreign_keys=[user_id],
        lazy="raise_on_sql",
    )
