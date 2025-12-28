from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...dependencies.current_user import get_current_user
from ...models.todos import Todos
from ...services.redirection import redirect_to_login


class TodoPageService:
    def __init__(self, db: Session):
        self.db = db
        self.templates = Jinja2Templates(
            directory="TodoAppPetProject/templates"
        )

    async def get_page(self, request: Request):
        try:
            user = await get_current_user(request.cookies.get("access_token"))

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
