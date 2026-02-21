from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, Integer, orm

from src.core.database import Base, mixins


class ReferralStatusType(StrEnum):
    active = "active"
    rewarded = "rewarded"


class Referral(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    status: orm.Mapped[ReferralStatusType] = orm.mapped_column(
        Enum(ReferralStatusType),
        default=ReferralStatusType.active,
    )

    user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    referrer_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("user.id"), nullable=False, unique=True)

    user = orm.relationship(
        "User",
        back_populates="referrals",
        foreign_keys=[user_id],
        lazy="selectin",
    )
    referrer = orm.relationship(
        "User",
        foreign_keys=[referrer_id],
        lazy="selectin",
    )
