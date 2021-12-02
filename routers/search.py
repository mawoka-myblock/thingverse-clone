import hashlib
import json
import uuid
from typing import Union
from datetime import datetime, timedelta
import os
import re
import io

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from fastapi.responses import RedirectResponse, PlainTextResponse, JSONResponse
from helpers.config import settings, col, minio
from helpers.models import *
import zipfile
from helpers.security.verify import send_mail
from helpers.security.auth import get_current_user, get_password_hash, get_user_from_id, verify_password, \
    create_access_token, get_user_from_mail, get_user_from_username, authenticate_user
from helpers.search import search_thing


router = APIRouter()

@router.get("/things")
async def thing_search(query: str, limit: Optional[int] = 10, category: Optional[str] = "all"):
    return await search_thing(query, limit, category)

