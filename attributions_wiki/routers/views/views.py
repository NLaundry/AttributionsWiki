"""This file contains all the views."""
# TODO: Break this up into more view files ... this will do for now though
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from prisma.models import Belief
from prisma.types import BeliefWhereUniqueInput

from ...db import db

templates = Jinja2Templates(directory="static/templates")
router = APIRouter(
    tags=["views"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Response:
    """Home testing."""
    template: Response = templates.TemplateResponse(  # type: ignore
        name="Home.html", context={"request": request}, status_code=200
    )
    return template


@router.get("/templates/belief/get_all", response_class=HTMLResponse)
async def get_all_beliefs_template(request: Request) -> Response:
    """Get HTMX for all beliefs."""
    beliefs: List[Belief] = await db.belief.find_many()
    template: Response = templates.TemplateResponse(  # type: ignore
        name="belief_list.html",
        context={"request": request, "beliefs": beliefs},
        status_code=200,
    )  # type: ignore
    return template


@router.get("/templates/belief/get/{id}", response_class=HTMLResponse)
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
