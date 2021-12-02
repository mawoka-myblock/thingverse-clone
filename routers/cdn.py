import json

from fastapi import APIRouter, BackgroundTasks, Header, File, UploadFile, Depends
from helpers.models import *
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
from helpers.config import settings, minio, col
from helpers.security.auth import get_current_user
import hashlib
import os
import io
import minio as Minio
import zipfile

router = APIRouter()


async def download_counter(thing: str, inc: bool = True):
    if inc:
        col("things").update_one({"id": thing}, {"$inc": {"downloads": 1}})
    else:
        col("things").update_one({"id": thing}, {"$inc": {"downloads": -1}})

@router.post("/upload")
async def upload(files: List[UploadFile] = File(...),
                 current_user: UserInDB = Depends(get_current_user)):
    buff = io.BytesIO()
    files_ok = True
    file_hashes = []
    for file in files:
        file_hashes.append(hashlib.md5(await file.read()).hexdigest())
        if not str(file.filename).lower().endswith(".stl"):
            files_ok = False
    files_ok = True
    if files_ok:
        zip_archive = zipfile.ZipFile(buff, mode='x', strict_timestamps=False)
        for file in files:
            file_content = await file.read()
            zip_archive.writestr(file.filename, file_content)
        zip_archive.close()
        bucket = settings.minio_bucket

        object_id = os.urandom(16).hex()
        zip_hash = hashlib.md5(str(file_hashes.sort()).encode("utf-8")).hexdigest()
        if await col("files").find_one({"hashsum": zip_hash}) is not None:
            return JSONResponse(status_code=409, content={"details": "File already exists"})
        minio.put_object(
            bucket_name=bucket,
            data=io.BytesIO(buff.getvalue()),
            length=len(buff.getvalue()),
            object_name=f"{current_user.username}/{object_id}.zip",
        )
        file_data = BaseFile(creation_date=str(datetime.now().replace(microsecond=0)), hash=zip_hash,
                             file_id=object_id, user_id=current_user.id)

        await col("files").insert_one(file_data.dict())

        return {"id": object_id}
    else:
        return JSONResponse({"details": "No stl-files provided"}, 400)


@router.get("/download/{user}/{object_id}", response_class=StreamingResponse)
async def download(user: str, object_id: str, background_tasks: BackgroundTasks):
    bucket = settings.minio_bucket
    try:
        background_tasks.add_task(download_counter, thing=object_id, inc=True)
        return StreamingResponse(
            minio.get_object(bucket_name=bucket, object_name=f"{user}/{object_id}.zip"),
            media_type="application/zip",
        )
    except Minio.error.S3Error as e:
        background_tasks.add_task(download_counter, thing=object_id, inc=False)
        if "NoSuchKey" in str(e):
            return JSONResponse(status_code=404, content={"details": "File not found"})
        else:
            return JSONResponse(status_code=500, content={"details": "Internal server error"})
