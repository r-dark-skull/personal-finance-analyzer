import os
from fastapi import APIRouter, Request
from models import *
from typing import List
from logging import getLogger
from datetime import datetime


logger = getLogger(__name__)

TRANSACTION_COLLECTION = os.getenv('TRANSACTION_COLLECTION')
router = APIRouter()


@router.get("/{start}/{end}", response_model=List[Transaction],
            response_description="List of all Transactions")
async def fetch_all_transactions(start: str, end: str, request: Request):
    return Transaction.find({
        "date": {
            "$gte": datetime.strptime(start, "%Y-%m-%d"),
            "$lt": datetime.strptime(end, "%Y-%m-%d")
        }
    })


@router.post("/{id}", response_description="Update a Transaction")
async def update_transaction(id: str, request: Request):

    try:
        transaction = await request.json()

        if not isinstance(transaction, dict):
            return {"status": "fail"}

        # parse date
        transaction['date'] = datetime.strptime(
            transaction["date"], "%Y-%m-%d")

        trx = Transaction(**transaction)

        assert trx.id == id

        return {"status": "success" if trx.update() == 1 else "fail"}
    except AssertionError as ase:
        logger.error(f"Tried to update different Document : {ase}")
        return {"status": "fail"}
    except Exception as e:
        logger.error(f"Error in request : {e}")
        return {"status": "fail"}
