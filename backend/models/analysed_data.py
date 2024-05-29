from pydantic import Field
from base import MongoDocument
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    CREDIT = "CR"
    DEBIT = "DR"


class Transaction(MongoDocument):
    id: str = Field(alias="_id")
    amount: float | None = Field(default=None)
    tx_type: TransactionType = Field(default=TransactionType.DEBIT)
    vendor: str | None = Field(default=None)
    category: str | None = Field(default=None)
    date: datetime | None = Field(default=None)
    vendor_id: str | None = Field(default=None)
