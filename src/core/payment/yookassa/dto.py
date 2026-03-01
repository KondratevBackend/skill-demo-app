from typing import Optional

from pydantic import BaseModel, Field


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
    internal_payment_id: int


class PaymentYookassaConfirmationRedirectDTO(BaseModel):
    type: str = Field(default="redirect")
    locale: Optional[str] = Field(default="ru_RU")
    return_url: str


class PaymentYookassaPayloadDTO(BaseModel):
    amount: PaymentYookassaAmountDTO
    description: Optional[str]
    # TODO: receipt: Optional[PaymentYookassaReceiptDTO]
    # TODO: metadata: PaymentYookassaMetadataDTO
    capture: bool = Field(default=True, description="Автоматический прием поступившего платежа")
    confirmation: Optional[PaymentYookassaConfirmationRedirectDTO]
