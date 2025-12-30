"""A collection of authentication-related APIs."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from dependencies.database.db import auth_service_dependency
from schemas.users import CreateUserRequest

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="templates")


### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    """HTTP frontend endpoint for rendering the login page template.

    Args:
        request (Request): The HTTP request object representing the
            client's request.

    Returns:
        TemplateResponse: An object rendering the "login.html" template.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    """HTTP frontend endpoint for rendering the register page template.

    Args:
        request (Request): The HTTP request object representing the
            client's request.

    Returns:
        TemplateResponse: An object rendering the "register.html"
            template.
    """
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints ###
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest, service: auth_service_dependency
) -> None:
    """HTTP backend endpoint for new user creation request.

    Args:
        request (CreateUserRequest): The user creation request schema.
        service (AuthServices): A business logic layer dependency used
            to create user profile.

    Returns:
        None
    """
    service.create(request)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    service: auth_service_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict:
    """HTTP backend endpoint for token authentication.

    Use user-provided credentials.

    Args:
        service (AuthServices): A business logic layer dependency used
            to generate an access token.
        form_data (OAuth2PasswordRequestForm): The user credentials
            (username and password) provided in the request.

    Returns:
         dict: An access token and its type.

    Raises:
        HTTPException: If authentication fails.
    """
    return service.access_token(form_data)
