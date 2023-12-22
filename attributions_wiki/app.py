"""Main FastAPI application."""
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

# from os import name
from typing import Annotated, Dict, List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from prisma import Prisma
from prisma.models import Attribution, Belief, Factor, User
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
    UserCreateInput,
    UserUpdateInput,
    UserWhereUniqueInput,
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO: these need to go in a .env file ... probably
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# TODO: Move to user auth or some sort of util file.
# TODO: type this
# made these internal methods ... front end should not have access to these
def _verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str):
    return pwd_context.hash(password)  # would need this for creation of user

async def get_user_by_username(username: str):
    user_obj: UserWhereUniqueInput = {"email": username}
    user: User = await db.user.find_unique_or_raise(user_obj) #type: ignore
    return user

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username) # check if exists
    print(user)
    print(password)
    print(_get_password_hash(password))
    if not user:
        return False
    if not _verify_password(plain_password=password, hashed_password=user.password): # check if got the right password, #hashed password is stored in DB so it comes with the user
        return False 
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Recall that username is a required field by ouath ... their username is their email
    # This is going to cause some WTFs
    # TODO: how do I indicate that username and email are the same thing?
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/create")
async def create_user(user_data: UserCreateInput) -> User:
    """Create a new user.

    Args: user_data: UserCreateInput
    Returns: User
    """
    print(user_data)
    user_data["password"] = _get_password_hash(user_data["password"])
    new_user: User = await db.user.create(user_data)
    return new_user




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
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor = await db.factor.find_unique_or_raise(id_obj)  # type: ignore
    return factor


@app.delete("/factor/delete/{id}")
async def delete_factor_by_id(id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.delete(id_obj)  # type: ignore
    return factor


@app.put("/factor/update/{id}")
async def update_factor(data: FactorUpdateInput, id: int) -> Factor | None:
    id_obj: FactorWhereUniqueInput = FactorWhereUniqueInput(id=id)  # type: ignore
    factor: Factor | None = await db.factor.update(data=data, where=id_obj)  # type: ignore
    return factor
