from sqlalchemy import BigInteger, ForeignKey, Integer, String, orm

from src.core.database import Base, mixins


class User(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    telegram_id: orm.Mapped[int] = orm.mapped_column(BigInteger)
    user_name: orm.Mapped[str] = orm.mapped_column(String(length=512), nullable=False)
    first_name: orm.Mapped[str] = orm.mapped_column(String(length=512), nullable=True)
    last_name: orm.Mapped[str] = orm.mapped_column(String(length=512), nullable=True)
    email: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=True)
    phone: orm.Mapped[str] = orm.mapped_column(String(length=128), nullable=True)

    server_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("server.id"), nullable=True)

    server = orm.relationship(
        "Server",
        back_populates="users",
        foreign_keys=[server_id],
        lazy="raise_on_sql",
    )
    referrals = orm.relationship(
        "Referral",
        back_populates="user",
        foreign_keys="[Referral.user_id]",
        lazy="raise_on_sql",
    )
    payments = orm.relationship(
        "Payment",
        back_populates="user",
        foreign_keys="[Payment.user_id]",
        lazy="raise_on_sql",
    )
    subscriptions = orm.relationship(
        "Subscription",
        back_populates="user",
        foreign_keys="[Subscription.user_id]",
        lazy="raise_on_sql",
    )
    lead = orm.relationship(
        "LeadUser",
        back_populates="user",
        foreign_keys="[LeadUser.user_id]",
        uselist=False,
        lazy="raise_on_sql",
    )
