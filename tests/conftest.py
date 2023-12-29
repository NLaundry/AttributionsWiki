import asyncio
import os
from typing import AsyncGenerator, Iterator

import pytest
from fastapi.testclient import TestClient

from attributions_wiki.app import app
from prisma import Prisma, register

# from server.database.base import *
# from server.config.exceptions import configure_exception_handlers
# from server.config.settings import settings
# from server.apis import apis


# def start_application() -> FastAPI:
#     """
#     Return a FastAPI app
#     """
#     _app = FastAPI(
#         title=str(settings.TITLE),
#         description=str(settings.DESCRIPTION),
#         version=str(settings.VERSION),
#     )
#     configure_exception_handlers(_app)
#     _app.include_router(apis)
#     return _app


TEST_DB_DSN = os.getenv("TEST_DATABASE_URL")
prisma = Prisma(datasource={"url": TEST_DB_DSN})


# async def initialize_db() -> None:
#     """
#     Initialize the test database
#     """
#     print("Initializing")
#     print("Creating all tables")
#     stream = os.popen(f"dotenv -e .env.test prisma db push --skip-generate")
#     output = stream.read()
#     print(output)


# async def teardown_db(client: Prisma) -> None:
#     """
#     Teardown the test database
#     """
#     print("Teardown")
#     print("Dropping all tables")
#     stream = os.popen(
#         f'dotenv -e .env.test prisma db execute --url "{TEST_DB_DSN}" --file "./server/tests/utils/reset_db.sql" '
#     )
#     print("Creating all tables")
#     stream = os.popen(f"DB_DSN={TEST_DB_DSN} prisma db push --skip-generate")
#     output = stream.read()
#     print(output)


# @pytest.fixture(scope="session")
# def app() -> Generator[FastAPI, Any, None]:
#     """
#     Initialize the app
#     """
#     _app = start_application()
#     yield _app


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Initialize the event loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop
    loop.close()


# Test client
@pytest.fixture(scope="session")
async def client(event_loop: asyncio.BaseEventLoop) -> AsyncGenerator[TestClient, None]:
    """Initialize the test client."""
    # await initialize_db()
    register(prisma)
    await prisma.connect()
    with TestClient(app) as c:
        yield c
    await prisma.disconnect()
    # await teardown_db(client=prisma)
