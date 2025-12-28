from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .dependencies.database.database import Base, engine
from .routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount(
    "/static", StaticFiles(directory="TodoAppPetProject/static"), name="static"
)


@app.get("/")
async def home():
    return RedirectResponse(
        url="/todos/todo-page", status_code=status.HTTP_302_FOUND
    )


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK"}


app.include_router(auth.router)
app.include_router(todos.router)

app.include_router(admin.router)

app.include_router(users.router)
