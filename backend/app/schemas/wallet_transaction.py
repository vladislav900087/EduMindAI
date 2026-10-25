from pydantic import BaseModel, ConfigDict, model_validator
from backend.app.models.course_purchase import Currency
from datetime import datetime


class WalletBalanceRead(BaseModel):

    KZT: int
    EUR: int

    model_config = ConfigDict(from_attributes=True)


class WalletTransactionTopUp(BaseModel):
    amount: int
    currency: Currency

    @model_validator(mode='after')
    def validate_amount_and_currency(self):
        if self.amount <= 0:
            raise ValueError('Amount must be greater than 0')

        if self.currency not in (Currency.EUR, Currency.KZT):
            raise ValueError('Currency must be EUR or KZT')

        return self


class WalletTransactionRead(BaseModel):

    id: int
    user_id: int
    purchase_id: int | None
    amount: int
    currency: str
    transaction_type: str
    direction: str
    status: str
    created_at: datetime




