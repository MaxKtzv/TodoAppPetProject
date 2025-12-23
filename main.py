from fastapi import FastAPI

from .dependencies.database.database import engine
from .models import Base
from .routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK"}


app.include_router(auth.router)
app.include_router(todos.router)

app.include_router(admin.router)

app.include_router(users.router)
