import hashlib
import json
import uuid
from typing import Union
from datetime import datetime, timedelta
import os
import re
import io

import bson.errors
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from fastapi.responses import RedirectResponse, PlainTextResponse, JSONResponse
from helpers.config import settings, col, minio
from helpers.models import *
import zipfile
from helpers.security.verify import send_mail
from helpers.security.auth import get_current_user, get_password_hash, get_user_from_id, verify_password, \
    create_access_token, get_user_from_mail, get_user_from_username, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/create", response_model=PublicThing)
async def create_thing(background_tasks: BackgroundTasks, data: BaseInputThing,
                       current_user: UserInDB = Depends(get_current_user)):
    # --- START checking for duplication, etc.
    thing_hash = hashlib.md5(json.dumps(data.dict(exclude={"pictures"})).encode()).hexdigest()
    for pic in data.pictures:
        if re.findall(r"((http:|https:)\/\/i\.imgur\.com\/)", pic) is []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid picture")
    if await col("files").find_one({"_id": ObjectId(data.file)}) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File does not exist")
    if await col("things").find_one({"hash": thing_hash}) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Thing already exists")

    # --- END checking for duplication, etc.
    creation_date = str(datetime.now().replace(microsecond=0).isoformat())
    thing_dict = {}
    thing_dict.update(data.dict())

    thing_dict.update(
        {"creation_date": creation_date, "user_id": current_user.id, "hash": thing_hash})
    thing = BaseThing(**thing_dict)
    await col("things").insert_one(thing.dict(by_alias=True))

    return PublicThing(**thing.dict())


@router.get("/thing/{thing_id}", response_model=PublicThing)
async def get_thing(thing_id: str):
    try:
        thing = await col("things").find_one({"_id": ObjectId(thing_id)})
    except bson.errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    if thing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing does not exist")
    return PublicThing(**thing)


@router.get("/like/{thing_id}")
async def like_thing(thing_id: str, background_tasks: BackgroundTasks,
                     current_user: UserInDB = Depends(get_current_user), ):
    async def bg_task():
        await col("likes").update_one({"_id": ObjectId(thing_id)},
                                      {"$addToSet": {"ids": current_user.id}}, upsert=True)
        await col("likes").update_one({"_id": ObjectId(thing_id)}, {"$addToSet": {"usernames": current_user.username}},
                                      upsert=True)
        await col("things").update_one({"_id": ObjectId(thing_id)}, {"$inc": {"like_count": 1}})

    thing = await col("things").find_one({"_id": ObjectId(thing_id)})
    if thing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thing does not exist")
    elif await col("likes").find_one({"usernames": {"$regex": str(current_user.username)}, "_id": ObjectId(thing_id)}) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already liked this thing")
    background_tasks.add_task(bg_task)

