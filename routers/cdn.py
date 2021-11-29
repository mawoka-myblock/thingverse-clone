from fastapi import APIRouter, BackgroundTasks, Header, File, UploadFile, Depends
from helpers.models import *
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from typing import Optional, List
from helpers.config import settings, minio
from helpers.security.auth import get_current_user
import os
import io
import minio as Minio
import zipfile

router = APIRouter()


@router.post("/upload")
async def upload(files: List[UploadFile] = File(...),
                 current_user: BaseUserCreate = Depends(get_current_user)):
    object_ids = []
    buff = io.BytesIO()
    zip_archive = zipfile.ZipFile(buff, mode='w')
    for file in files:

        file_content = await file.read()
        file_size = len(file_content)
        zip_archive.writestr(file.filename, file_content)
    zip_archive.close()
    bucket = settings.minio_bucket

    object_id = os.urandom(16).hex()
    minio.put_object(
        bucket_name=bucket,
        data=io.BytesIO(buff.getvalue()),
        length=len(buff.getvalue()),
        object_name=f"{current_user.username}/{object_id}.zip",
    )

    return {"id": object_id}


@router.get("/download/{user}/{object_id}", response_class=StreamingResponse)
async def download(user: str, object_id: str):
    bucket = settings.minio_bucket
    try:
        return StreamingResponse(
            minio.get_object(bucket_name=bucket, object_name=f"{user}/{object_id}.zip"),
            media_type="application/zip",
        )
    except Minio.error.S3Error as e:
        if "NoSuchKey" in str(e):
            return JSONResponse(status_code=404, content={"details": "File not found"})
        else:
            return JSONResponse(status_code=500, content={"details": "Internal server error"})
