import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import MongoClient
from .transaction_routes import router
from .analysis_routes import router as analysis_router
from server import context, credentials


@asynccontextmanager
async def lifespan(app: FastAPI):
    # url = os.getenv('MONGO_URL_TEMPLATE')
    mongodb_client = MongoClient(
        credentials['auth']['db']['mongo']['connection_string'])

    app.mongodb_client = mongodb_client
    app.database = app.mongodb_client[os.getenv('MONGO_DATABASE')]

    app.include_router(router, prefix="/transactions")
    app.include_router(analysis_router, prefix="/analysis")

    # server context
    context.update(
        mongodb_client=mongodb_client,
        database=mongodb_client[os.getenv('MONGO_DATABASE')]
    )

    yield
    app.mongodb_client.close()


def create_app():
    app = FastAPI(lifespan=lifespan)

    # setting up jobs
    os.system("/develop/jobs/setup.sh")

    return app
