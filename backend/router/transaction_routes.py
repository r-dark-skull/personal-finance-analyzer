import os
from fastapi import APIRouter, Request
from models import *
from typing import List


TRANSACTION_COLLECTION = os.getenv('TRANSACTION_COLLECTION')
router = APIRouter()


@router.get("/", response_model=List[Transaction], response_description="List of all Transactions")
async def fetch_all_transactions(request: Request):
    transactions = list(
        request.app.database[TRANSACTION_COLLECTION].find(limit=100))
    return transactions


@router.post("/{id}", response_model=Transaction, response_description="Update a Transaction")
async def update_transaction(id: str, request: Request):
    transaction = await request.json()

    if len(transaction) >= 1:
        updates = request.app.database[TRANSACTION_COLLECTION].update_one(
            {"_id": id}, {"$set": transaction}
        )

    if (
        existing_transaction := request.app.database[TRANSACTION_COLLECTION].find_one({"_id": id})
    ) is not None:
        return existing_transaction
    else:
        return {}
