from sqlalchemy import ForeignKey, Integer, String, orm

from src.core.database import Base, mixins


class Coupon(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    code: orm.Mapped[str] = orm.mapped_column(String(length=128), unique=True, nullable=False)

    tariff_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("tariff.id"), nullable=False)

    tariff = orm.relationship(
        "Tariff",
        back_populates="coupons",
        foreign_keys=tariff_id,
        lazy="selectin",
    )
