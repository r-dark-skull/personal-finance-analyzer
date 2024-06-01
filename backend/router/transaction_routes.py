import os
from fastapi import APIRouter, Request
from models import *
from typing import List
from logging import getLogger
from datetime import datetime
from pymongo.errors import DuplicateKeyError


logger = getLogger(__name__)

TRANSACTION_COLLECTION = os.getenv('TRANSACTION_COLLECTION')
router = APIRouter()


@router.get("/{start}/{end}", response_model=List[Transaction],
            response_description="List of all Transactions")
async def fetch_all_transactions(start: str, end: str, request: Request):
    return Transaction.find({
        "date": {
            "$gte": datetime.strptime(start, "%Y-%m-%d"),
            "$lte": datetime.strptime(end, "%Y-%m-%d")
        },
        "$or": [{
                "is_deleted": {
                    "$exists": False
                }}, {
            "is_deleted": False
        }]
    })


@router.post("/{id}", response_description="Update a Transaction")
async def update_transaction(id: str, request: Request):

    try:
        transaction = await request.json()

        if not isinstance(transaction, dict):
            return {"status": "fail"}

        original = Transaction.find({"_id": id})[0]

        # removing disabled options
        transaction = {
            **transaction,
            "_id": original.id,
            "amount": original.amount,
            "date": original.date,
            "is_deleted": original.is_deleted
        }

        trx = Transaction(**transaction)

        assert trx.id == id

        return {"status": "success" if trx.update() == 1 else "fail"}
    except AssertionError as ase:
        logger.error(f"Tried to update different Document : {ase}")
        return {"status": "fail"}
    except Exception as e:
        logger.error(f"Error in request : {e}")
        return {"status": "fail"}


@router.post("/delete/{id}")
async def delete_transaction(id: str, request: Request):
    try:
        transaction = await request.json()
        assert isinstance(transaction, dict)

        original = Transaction.find({"_id": id})[0]
        original.is_deleted = True

        return {"status": "success" if original.update() == 1 else "fail"}

    except Exception as e:
        logger.error(e)
        return {"status": "fail"}


@router.post("/add/new")
async def add_transaction(request: Request):
    try:
        transaction = await request.json()
        logger.info(f'New Transation Data : {transaction}')
        assert isinstance(transaction, dict)

        if Transaction.find({"_id": transaction.get("_id")}):
            raise DuplicateKeyError()

        trx = Transaction(**transaction)

        trx.insert()
        logger.info(f"Transaction Inserted : {trx.id}")

    except Exception as e:
        logger.error(f"Err NEW Transaction : {e}")
