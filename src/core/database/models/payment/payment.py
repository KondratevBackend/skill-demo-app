import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, orm

from src.core.database import Base, mixins
from src.core.database.models.payment.provider import PaymentProviderType


class PaymentStatusType(StrEnum):
    pending = "pending"
    succeeded = "succeeded"
    refunded = "refunded"
    failed = "failed"


class Payment(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    amount: orm.Mapped[float] = orm.mapped_column(Float, nullable=False)
    currency: orm.Mapped[str] = orm.mapped_column(String(length=64), nullable=False)
    provider: orm.Mapped[PaymentProviderType] = orm.mapped_column(Enum(PaymentProviderType), nullable=False)
    provider_payment_id: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=False)
    status: orm.Mapped[PaymentStatusType] = orm.mapped_column(Enum(PaymentStatusType), nullable=False)
    payment_method: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=True)
    paid_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime, nullable=True)

    tariff_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("tariff.id"))
    user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    tariff = orm.relationship(
        "Tariff",
        back_populates="payments",
        foreign_keys=[tariff_id],
        lazy="raise_on_sql",
    )
    user = orm.relationship(
        "User",
        back_populates="payments",
        foreign_keys=[user_id],
        lazy="raise_on_sql",
    )
