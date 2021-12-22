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


@router.get("/my")
async def get_my_cols(current_user: UserInDB = Depends(get_current_user)):
    return_obs = []
    for doc in await col("collections").find({"username": current_user.username}).to_list(length=None):
        return_obs.append(PublicCollection(**doc))
    return return_obs


@router.get("/{col_id}")
async def get_col(col_id: str):
    doc = await col("collections").find_one({"_id": ObjectId(col_id)})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return PublicCollection(**doc)


@router.put("/{col_id}/update")
async def add_item_to_col(col_id: str, thing: str, background_tasks: BackgroundTasks,
                          current_user: UserInDB = Depends(get_current_user)):
    doc = await col("collections").find_one({"_id": ObjectId(col_id)})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    if doc["username"] != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do that")
    if await col("things").find_one({"_id": ObjectId(thing)}) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing not found")
    await col("collections").update_one({"_id": ObjectId(col_id)}, {"$addToSet": {"things": ObjectId(thing)}})


@router.delete("/{col_id}/delete")
async def delete_item_from_col(col_id: str, thing: str, current_user: UserInDB = Depends(get_current_user)):
    doc = await col("collections").find_one({"_id": ObjectId(col_id)})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    if doc["username"] != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do that")
    await col("collections").update_one({"_id": ObjectId(col_id)}, {"$pull": {"things": ObjectId(thing)}})


@router.delete("/{col_id}/delete_collection")
async def delte_collection(col_id: str, current_user: UserInDB = Depends(get_current_user)):
    doc = await col("collections").find_one({"_id": ObjectId(col_id)})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    if doc["username"] != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do that")
    await col("collections").delete_one({"_id": ObjectId(col_id)})
