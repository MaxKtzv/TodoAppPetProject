from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..dependencies.user import get_current_user
from ..models import Todos

templates = Jinja2Templates(directory="TodoAppPetProject/templates")


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


async def check_and_render(request, db, todo_id, html):
    try:
        token = request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        user = await get_current_user(token)
        if html == "todo.html":
            todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
            return templates.TemplateResponse(
                html,
                {"request": request, "todos": todos, "user": user},
            )
        if html == "add-todo.html":
            return templates.TemplateResponse(html, {"request": request, "user": user})
        if html == "edit-todo.html":
            todo = db.query(Todos).filter(Todos.id == todo_id).first()
            return templates.TemplateResponse(
                html,
                {"request": request, "todo": todo, "user": user},
            )
    except Exception:
        return redirect_to_login()
