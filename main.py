from fastapi import FastAPI
from routers import users
from routers import cdn

app = FastAPI(redoc_url="")

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(cdn.router, prefix="/api/v1/cdn")
