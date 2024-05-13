import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import MongoClient
from .routes import router
from server import context


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = os.getenv('MONGO_URL_TEMPLATE')
    mongodb_client = MongoClient(url.format(
        username=os.getenv('MONGO_USERNAME'),
        password=os.getenv('MONGO_PASSWORD'),
        address=os.getenv('MONGO_SOCKET_ADDRESS')
    ))

    app.mongodb_client = mongodb_client
    app.database = app.mongodb_client[os.getenv('MONGO_DATABASE')]

    app.include_router(router, prefix="/transactions")

    # server context
    context.update(
        mongodb_client=mongodb_client,
        database=mongodb_client[os.getenv('MONGO_DATABASE')]
    )

    yield
    app.mongodb_client.close()


def create_app():
    app = FastAPI(lifespan=lifespan)

    return app
