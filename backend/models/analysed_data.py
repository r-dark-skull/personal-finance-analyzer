from pydantic import BaseModel, Field
from datetime import date as date_type
from enum import Enum


class TransactionType(str, Enum):
    CREDIT = "CR"
    DEBIT = "DR"


class Transaction(BaseModel):
    id: str = Field(alias="_id")
    amount: float | None = Field(default=None)
    tx_type: TransactionType = Field(default=TransactionType.DEBIT)
    vendor: str | None = Field(default=None)
    category: str | None = Field(default=None)
    date: date_type | None = Field(default=None)
    vendor_id: str | None = Field(default=None)

    class Config:
        populate_by_name = True
