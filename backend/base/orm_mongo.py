from typing import Any
from pydantic import BaseModel, Field
from pymongo.database import Database


class MongoDocument(BaseModel):
    id: str = Field(alias='_id')

    class Config:
        populate_by_name = True

    @classmethod
    def register(cls, database: Database, collection_name: str):
        cls._db = database
        cls._collection = cls._db.get_collection(collection_name)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

    def save(self, upsert=True):
        result = self._collection.update_one(
            {"_id": self.id},
            {"$set": self.model_dump(by_alias=True)},
            upsert=upsert
        )

        return result.modified_count or result.upserted_id

    def insert(self):
        result = self._collection.insert_one(self.model_dump(by_alias=True))
        assert result.inserted_id == self.id

    def update(self):
        return self.save(upsert=False)

    @classmethod
    def find(cls, filters: dict):
        return [cls(**document) for document in cls._collection.find(filters)]
