from sqlalchemy import Boolean, CheckConstraint, Integer, String, orm

from src.core.database import Base, mixins


class Feedback(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    rating: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    user_name: orm.Mapped[str] = orm.mapped_column(String(length=64), nullable=True)
    advantages: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    flaws: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    comment: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    is_published: orm.Mapped[bool] = orm.mapped_column(Boolean, default=False)
    is_verified_user: orm.Mapped[bool] = orm.mapped_column(Boolean, default=False)

    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),)
