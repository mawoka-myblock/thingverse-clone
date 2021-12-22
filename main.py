from fastapi import FastAPI
from routers import users
from routers import cdn, things, search, collections
from helpers.config import settings, minio

app = FastAPI(redoc_url="")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(cdn.router, prefix="/api/v1/cdn", tags=["cdn"])
app.include_router(things.router, prefix="/api/v1/things", tags=["things"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(collections.router, prefix="/api/v1/collections", tags=["collections"])


@app.on_event("startup")
async def startup_check():
    if not minio.bucket_exists(settings.minio_bucket):
        minio.make_bucket(settings.minio_bucket)
