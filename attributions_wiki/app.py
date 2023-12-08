from contextlib import asynccontextmanager
from os import name
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prisma import Prisma
from prisma.enums import Role
from prisma.models import Factor, User
from prisma.types import UserCreateInput

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def home() -> str:
    """Home testing."""
    return "Hello world"

@app.get("/user/create_test")
async def create_user_test() -> User:
    """Home testing."""
    new_user: User = await db.user.create( data={
        'name':  'franklin',
        'email': 'bob@gmail.com'
        })
    return new_user

@app.post("/user/create")
async def create_user(user_data: UserCreateInput) -> User:
    print(user_data)
    new_user: User = await db.user.create(user_data)
    return new_user


# @app.post("/todo/create")
# async def create_todo(new_todo: TodoCreateInput) -> Todo:
#     created_todo = await db.todo.create(new_todo)
#     return created_todo

# @app.get("/todo/read_all")
# async def read_all_todo() -> List[Todo]:
#     todo_list: List[Todo] = await db.todo.find_many()
#     return todo_list

