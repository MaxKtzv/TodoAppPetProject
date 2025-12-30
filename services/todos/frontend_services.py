"""Provides business logic handling for Todo application pages."""

from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies.current_user import get_current_user
from models.todos import Todos
from services.redirection import redirect_to_login


class TodoPageService:
    """Service class for managing and rendering todo-related pages.

    Attributes:
        db (Session): Database session for querying and manipulating
            data.
        templates (Jinja2Templates): The Jinja2 template rendering
            instance for page generation.
    """

    def __init__(self, db: Session):
        """Initialize the TodoPageService class."""

        self.db = db
        self.templates = Jinja2Templates(
            directory="templates"
        )

    async def get_page(self, request: Request):
        """Retrieve and render the todos list page.

        Args:
            request (Request): The HTTP request object.

        Returns:
            TemplateResponse: An object rendering the "todo.html" page if
                the user is authenticated.

        Raises:
            RedirectResponse: A HTTP redirect response to the login page
                if authentication fails.
        """
        try:
            user: dict = await get_current_user(
                request.cookies.get("access_token")
            )

            if user is None:
                return redirect_to_login()

            todos = (
                self.db.query(Todos)
                .filter(Todos.owner_id == user.get("id"))
                .all()
            )

            return self.templates.TemplateResponse(
                "todo.html",
                {"request": request, "todos": todos, "user": user},
            )

        except Exception:
            return redirect_to_login()

    async def add_page(self, request: Request):
        """Retrieve and render the add todo page.

        Args:
            request (Request): The HTTP request object.

        Returns:
            TemplateResponse: An object rendering the "add-todo.html" page
                if the user is authenticated.

        Raises:
            RedirectResponse: A HTTP redirect response to the login page
                if authentication fails.
        """
        try:
            user = await get_current_user(request.cookies.get("access_token"))

            if user is None:
                return redirect_to_login()

            return self.templates.TemplateResponse(
                "add-todo.html", {"request": request, "user": user}
            )

        except Exception:
            return redirect_to_login()

    async def edit_page(self, request: Request, todo_id: int):
        """Retrieve and render the edit todo page.

        Args:
            request (Request): The HTTP request object.
            todo_id (int): The ID of the todo to be edited.

        Returns:
            TemplateResponse: An object rendering the "edit-todo.html" page
                if the user is authenticated.

        Raises:
            RedirectResponse: A HTTP redirect response to the login page
                if authentication fails.
        """
        try:
            user = await get_current_user(request.cookies.get("access_token"))

            if user is None:
                return redirect_to_login()
            todo = self.db.query(Todos).filter(Todos.id == todo_id).first()
            return self.templates.TemplateResponse(
                "edit-todo.html",
                {"request": request, "todo": todo, "user": user},
            )

        except Exception:
            return redirect_to_login()
