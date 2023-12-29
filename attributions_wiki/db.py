from contextlib import asynccontextmanager

from fastapi import FastAPI

from prisma import Prisma

db = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to the database before running the test, then disconnect afterwards."""
    await db.connect()
    yield
    await db.disconnect()
