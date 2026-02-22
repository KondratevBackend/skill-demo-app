from sqlalchemy import Integer, String, orm

from src.core.database import Base, mixins


class Server(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    domain: orm.Mapped[str] = orm.mapped_column(String(length=64), nullable=False)
    connection_id: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    cookie: orm.Mapped[str] = orm.mapped_column(String(length=1024), nullable=True)

    users = orm.relationship(
        "User",
        back_populates="server",
        foreign_keys="[User.server_id]",
        lazy="raise_on_sql",
    )
