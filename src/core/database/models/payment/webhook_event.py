from typing import Optional

from sqlalchemy import JSON, Enum, String, orm

from src.core.database import Base, mixins
from src.core.database.models.payment.provider import PaymentProviderType


class WebhookEvent(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    provider: orm.Mapped[PaymentProviderType] = orm.mapped_column(Enum(PaymentProviderType), nullable=False)
    provider_event_id: orm.Mapped[str] = orm.mapped_column(String(length=256), nullable=False)
    event_type: orm.Mapped[str] = orm.mapped_column(String)
    signature: orm.Mapped[str] = orm.mapped_column(String)
    payload_json: orm.Mapped[Optional[JSON]] = orm.mapped_column(type_=JSON)
