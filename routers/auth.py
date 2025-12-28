from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from ..dependencies.database.db import auth_service_dependency
from ..schemas.token import Token
from ..schemas.users import CreateUserRequest

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="TodoAppPetProject/templates")


### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints ###
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest, service: auth_service_dependency
):
    return service.create(create_user_request)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    service: auth_service_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return service.access_token(form_data)
