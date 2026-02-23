from sqlalchemy import Boolean, Float, Integer, String, orm
from sqlalchemy import text as text_orm

from src.core.database import Base, mixins


class Tariff(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    text: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=False)
    days: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    price: orm.Mapped[float] = orm.mapped_column(Float, nullable=False)
    limit_ip: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    order_index: orm.Mapped[int] = orm.mapped_column(Integer, server_default="0", nullable=False)
    is_trial: orm.Mapped[bool] = orm.mapped_column(Boolean, server_default=text_orm("false"))
    is_popular: orm.Mapped[bool] = orm.mapped_column(Boolean, server_default=text_orm("false"))

    payments = orm.relationship(
        "Payment",
        back_populates="tariff",
        foreign_keys="[Payment.tariff_id]",
        lazy="raise_on_sql",
    )
    subscriptions = orm.relationship(
        "Subscription",
        back_populates="tariff",
        foreign_keys="[Subscription.tariff_id]",
        lazy="raise_on_sql",
    )
    coupons = orm.relationship(
        "Coupon",
        back_populates="tariff",
        foreign_keys="[Coupon.tariff_id]",
        lazy="raise_on_sql",
    )
