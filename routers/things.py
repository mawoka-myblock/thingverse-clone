import uuid
from typing import Union
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import RedirectResponse, PlainTextResponse, JSONResponse
from helpers.config import settings, col
from helpers.models import *
from helpers.security.verify import send_mail
from helpers.security.auth import get_current_user, get_password_hash, get_user_from_id, verify_password, \
    create_access_token, get_user_from_mail, get_user_from_username, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/create")
async def create_thing(data: BaseInputThing, current_user: BaseUserCreate = Depends(get_current_user)):
    pass
