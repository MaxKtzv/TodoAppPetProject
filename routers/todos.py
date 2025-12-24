from fastapi import APIRouter, HTTPException, Path, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..dependencies.database.db import db_dependency
from ..dependencies.user import get_current_user, user_dependency
from ..models import Todos
from ..schemas import TodoRequest, TodoResponse
from ..services.todo_search import find_todo

templates = Jinja2Templates(directory="TodoAppPetProject/templates")

router = APIRouter(prefix="/todos", tags=["todos"])


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        user = await get_current_user(token)
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse(
            "todo.html",
            {"request": request, "todos": todos, "user": user},
        )
    except Exception as e:
        # Log the error here if you can to see why it's failing
        print(f"Error rendering todo page: {e}")
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        user = await get_current_user(token)
        return templates.TemplateResponse(
            "add-todo.html", {"request": request, "user": user}
        )
    except Exception as e:
        # Log the error here if you can to see why it's failing
        print(f"Error rendering todo page: {e}")
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}", status_code=status.HTTP_200_OK)
async def render_edit_todo_page(
    request: Request, todo_id: int, db: db_dependency
):
    try:
        token = request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        user = await get_current_user(token)

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse(
            "edit-todo.html", {"request": request, "todo": todo, "user": user}
        )
    except Exception as e:
        # Log the error here if you can to see why it's failing
        print(f"Error rendering todo page: {e}")
        return redirect_to_login()


### Endpoints ###
@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse]
)
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get(
    "/todo/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(ge=1),
):
    return find_todo(user, db, todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401)
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(ge=1),
):
    todo_model = find_todo(user, db, todo_id)

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(ge=1),
):
    todo_model = find_todo(user, db, todo_id)

    db.delete(todo_model)
    db.commit()
