import uuid
from pydantic import BaseModel, Field


class RawEmail(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sender: str
    mail_body: str
    date: str
    is_analyzed: bool = Field(default=False)
    is_transaction: bool | None = Field(default=None)

    class Config:
        populate_by_name = True
