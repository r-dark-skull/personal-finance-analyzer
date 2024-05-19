from uuid import uuid4
from pydantic import BaseModel, Field


class CategoryStore(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    category: str
    vendor_id: str

    class Config:
        populate_by_name = True
