from uuid import uuid4
from pydantic import Field
from base import MongoDocument


class CategoryStore(MongoDocument):
    id: str = Field(default_factory=uuid4, alias="_id")
    category: str
    vendor_id: str
