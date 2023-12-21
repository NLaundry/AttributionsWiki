"""Main FastAPI application."""
from contextlib import asynccontextmanager

# from os import name
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from prisma import Prisma
from prisma.models import Attribution, Belief, Factor

# from prisma.types import UserCreateInput
from prisma.types import (
    AttributionCreateInput,
    AttributionUpdateInput,
    AttributionWhereUniqueInput,
    BeliefCreateInput,
    BeliefUpdateInput,
    BeliefWhereUniqueInput,
    FactorCreateInput,
    FactorUpdateInput,
    FactorWhereUniqueInput,
)

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
    template: Response = templates.TemplateResponse(  # type: ignore
        name="Home.html", context={"request": request}, status_code=200
    )
    return template


@app.get("/templates/belief/get_all", response_class=HTMLResponse)
async def get_all_beliefs_template(request: Request) -> Response:
    """Get HTMX for all beliefs."""
    beliefs: List[Belief] = await db.belief.find_many()
    template: Response = templates.TemplateResponse(  # type: ignore
        name="belief_list.html",
        context={"request": request, "beliefs": beliefs},
        status_code=200,
    )  # type: ignore
    return template


@app.get("/templates/belief/get/{id}", response_class=HTMLResponse)
async def get_belief_by_id_template(request: Request, id: int) -> Response:
    """Get HTMX for single belief by id."""
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief = await db.belief.find_unique_or_raise(id_obj)
    template: Response = templates.TemplateResponse(  # type: ignore
        name="belief.html",
        context={"request": request, "belief": belief},
        status_code=200,
    )
    return template


@app.post("/belief/create")
async def create_belief(belief_data: BeliefCreateInput) -> Belief:
    """Create a new belief.

    Args: belief_data: BeliefCreateInput
    Returns: Belief
    """
    new_belief: Belief = await db.belief.create(belief_data)
    return new_belief


@app.get("/belief/get_all")
async def get_beliefs() -> List[Belief]:
    """Get all beliefs.

    Returns: List[Belief]
    """
    beliefs: List[Belief] = await db.belief.find_many()
    return beliefs


@app.get("/belief/get/{id}")
async def get_belief_by_id(id: int) -> Belief:
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief = await db.belief.find_unique_or_raise(id_obj)
    return belief


@app.delete("/belief/delete/{id}")
async def delete_belief_by_id(id: int) -> Belief | None:
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief | None = await db.belief.delete(id_obj)
    return belief


@app.put("/belief/update/{id}")
async def update_belief(data: BeliefUpdateInput, id: int) -> Belief | None:
    id_obj: BeliefWhereUniqueInput = BeliefWhereUniqueInput(id=id)
    belief: Belief | None = await db.belief.update(data=data, where=id_obj)
    return belief


# model Attribution {
#     id              Int             @id @default(autoincrement())
#     created_at      DateTime        @default(now())
#     updated_at      DateTime        @updatedAt
#     locus           Locus
#     stability       Stability
#     controllability Controllability
#     reason          String?
# }


@app.post("/attribution/create")
async def create_attribution(attribution_data: AttributionCreateInput) -> Attribution:
    """Create a new attribution.

    Args: attribution_data: AttributionCreateInput
    Returns: Attribution
    """
    new_attribution: Attribution = await db.attribution.create(attribution_data)
    return new_attribution


@app.get("/attribution/get_all")
async def get_attributions() -> List[Attribution]:
    """Get all attributions.

    Returns: List[Attribution]
    """
    attributions: List[Attribution] = await db.attribution.find_many()
    return attributions


@app.get("/attribution/get/{id}")
async def get_attribution_by_id(id: int) -> Attribution:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution = await db.attribution.find_unique_or_raise(id_obj)
    return attribution


@app.delete("/attribution/delete/{id}")
async def delete_attribution_by_id(id: int) -> Attribution | None:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.delete(id_obj)
    return attribution


@app.put("/attribution/update/{id}")
async def update_attribution(
    data: AttributionUpdateInput, id: int
) -> Attribution | None:
    id_obj: AttributionWhereUniqueInput = AttributionWhereUniqueInput(id=id)
    attribution: Attribution | None = await db.attribution.update(
        data=data, where=id_obj
    )
    return attribution


@app.post("/factor/create")
async def create_factor(factor_data: FactorCreateInput) -> Factor:
    """Create a new factor.

    Args: factor_data: FactorCreateInput
    Returns: Factor
    """
    new_factor: Factor = await db.factor.create(factor_data)
    return new_factor


@app.get("/factor/get_all")
async def get_factors() -> List[Factor]:
    """Get all factors.

    Returns: List[Factor]
    """
    factors: List[Factor] = await db.factor.find_many()
    return factors


@app.get("/factor/get/{id}")
async def get_factor_by_id(id: int) -> Factor:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id) #type: ignore
    factor: Factor = await db.factor.find_unique_or_raise(id_obj) #type: ignore
    return factor


@app.delete("/factor/delete/{id}")
async def delete_factor_by_id(id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id) #type: ignore
    factor: Factor | None = await db.factor.delete(id_obj) #type: ignore
    return factor


@app.put("/factor/update/{id}")
async def update_factor(data: FactorUpdateInput, id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.update(data=data, where=id_obj) # type: ignore
    return factor
