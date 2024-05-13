from pydantic import BaseModel, Field
from enum import Enum


class TransactionType(str, Enum):
    CREDIT = "CR"
    DEBIT = "DR"


class Transaction(BaseModel):
    id: str = Field(alias="_id")
    amount: float
    tx_type: TransactionType = Field(default=TransactionType.DEBIT)
    vendor: str
    vendor_id: str | None = Field(default=None)

    class Config:
        populate_by_name = True
