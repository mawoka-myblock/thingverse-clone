from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from helpers.config import col
from helpers.models import *
from helpers.security.auth import get_current_user

router = APIRouter()


@router.post("/create")
async def create_col(data: CreateCollection, background_tasks: BackgroundTasks,
                     current_user: UserInDB = Depends(get_current_user)):
    if await col("collections").find_one({"name": data.name}) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Collection already exists")
    dat = data.dict(by_alias=True)
    dat.update({"username": current_user.username, "creation_date": str(datetime.now().replace(microsecond=0))})
    db_data = PublicCollection(**dat)

    await col("collections").insert_one(db_data.dict(by_alias=True))
