import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.core.database.models import PaymentStatusType


class PaymentYookassaAmountDTO(BaseModel):
    value: float = Field(...)
    currency: str = Field(default="RUB", description="ISO-4217")


class PaymentYookassaReceiptCustomerDTO(BaseModel):
    full_name: str = Field(default="Не указал")
    inn: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class PaymentYookassaReceiptItemsDTO(BaseModel):
    description: str
    amount: PaymentYookassaAmountDTO
    vat_code: int = Field(..., description="Ставка НДС (тег в 54 ФЗ — 1199)")
    quantity: int = Field(1, description="Количество товара (тег в 54 ФЗ — 1023)")


class PaymentYookassaReceiptDTO(BaseModel):
    customer: Optional[PaymentYookassaReceiptCustomerDTO]
    items: PaymentYookassaReceiptItemsDTO
    internet: Optional[bool] = Field(
        default=True,
        description="Признак проведения платежа в интернете (тег в 54 ФЗ — 1125)",
    )
    tax_system_code: Optional[int] = Field(..., description="Система налогообложения магазина (тег в 54 ФЗ — 1055)")


class PaymentYookassaMetadataDTO(BaseModel):
    tariff_id: int
    user_id: int


class PaymentYookassaConfirmationRedirectDTO(BaseModel):
    type: str = Field(default="redirect")
    return_url: str


class PaymentYookassaPayloadDTO(BaseModel):
    amount: PaymentYookassaAmountDTO
    description: Optional[str]
    # TODO: receipt: Optional[PaymentYookassaReceiptDTO]
    metadata: PaymentYookassaMetadataDTO
    capture: bool = Field(default=True, description="Автоматический прием поступившего платежа")
    confirmation: Optional[PaymentYookassaConfirmationRedirectDTO]



class PaymentYookassaConfirmationDTO(BaseModel):
    type: str
    confirmation_url: str


class PaymentYookassaMethodDTO(BaseModel):
    type: str
    id: str
    saved: bool


class PaymentYookassaDTO(BaseModel):
    id: str
    amount: PaymentYookassaAmountDTO
    status: PaymentStatusType
    payment_method: Optional[PaymentYookassaMethodDTO] = Field(default=None)
    metadata: PaymentYookassaMetadataDTO
    confirmation: PaymentYookassaConfirmationDTO
    paid: bool
    test: bool
    refundable: bool
    description: Optional[str] = Field(default=None)
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = Field(default=None)
