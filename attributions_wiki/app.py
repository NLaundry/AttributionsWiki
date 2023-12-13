from contextlib import asynccontextmanager

# from os import name
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from prisma import Prisma
from prisma.models import Belief

# from prisma.types import UserCreateInput
from prisma.types import BeliefCreateInput, BeliefWhereUniqueInput, BeliefUpdateInput
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Response:
    """Home testing."""
    template: Response = templates.TemplateResponse(name ="Home.html", context = {"request": request}, status_code=200) #type: ignore
    return template 

@app.get("/templates/belief/get_all", response_class=HTMLResponse)
async def get_all_beliefs_template(request: Request) -> Response:
    beliefs: List[Belief] = await db.belief.find_many()
    template: Response = templates.TemplateResponse(name ="belief_list.html", context = {"request": request, "beliefs": beliefs}, status_code=200) #type: ignore
    return template



@app.post("/belief/create")
async def create_belief(belief_data: BeliefCreateInput) -> Belief:
    new_belief: Belief = await db.belief.create(belief_data)
    return new_belief


@app.get("/belief/get_all")
async def get_beliefs() -> List[Belief]:
    beliefs: List[Belief] = await db.belief.find_many()
    return beliefs


@app.get("/belief/get")
async def get_belief_by_id(id: BeliefWhereUniqueInput) -> Belief:
    belief: Belief = await db.belief.find_unique_or_raise(id)
    return belief


@app.delete("/belief/delete")
async def delete_belief_by_id(id: BeliefWhereUniqueInput) -> Belief | None:
    belief: Belief | None = await db.belief.delete(id)
    return belief


@app.put("/belief/update")
async def update_belief(
    data: BeliefUpdateInput, id: BeliefWhereUniqueInput
) -> Belief | None:
    belief: Belief | None = await db.belief.update(data=data, where=id)
    return belief
