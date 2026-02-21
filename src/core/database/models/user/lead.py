from sqlalchemy import orm, String, Integer, ForeignKey

from src.core.database import Base, mixins


class Lead(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    title: orm.Mapped[str] = orm.mapped_column(String(length=64), nullable=False)

    users = orm.relationship(
        "LeadUser",
        back_populates="lead",
        foreign_keys="[LeadUser.lead_id]",
        lazy="raise_on_sql",
    )


class LeadUser(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    lead_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("lead.id"), nullable=False)

    user = orm.relationship(
        "User",
        back_populates="lead",
        foreign_keys=user_id,
        uselist=False,
        lazy="raise_on_sql",
    )
    lead = orm.relationship(
        "Lead",
        back_populates="users",
        foreign_keys=lead_id,
        lazy="raise_on_sql",
    )
