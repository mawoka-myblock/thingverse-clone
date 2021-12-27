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


@router.post("/create", response_model=PublicUser)
async def create_user(user: BaseUserCreate, background_task: BackgroundTasks) -> Union[PublicUser, JSONResponse]:
    user_in_db = await get_user_from_mail(user.email)
    if user_in_db is not None:
        raise HTTPException(status_code=400, detail="User already registered")
    user.password = get_password_hash(user.password)
    if len(user.username) == 32:
        return JSONResponse({"details": "Username mustn't be 32 characters long"}, 400)
    userindb = UserInDB(**user.dict(), is_superuser=False, date_joined=str(datetime.now()))
    _id = await col("users").insert_one(userindb.dict())
    background_task.add_task(send_mail, email=user.email)
    user_dict = userindb.dict(by_alias=True)
    return PublicUser(**user_dict)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("expiry")
    return {"message": "Logged out"}


@router.get("/users/me/", response_model=PrivateUser)
async def read_users_me(current_user: BaseUserCreate = Depends(get_current_user)):
    return PrivateUser(**current_user.dict())


@router.get("/users/test-token")
async def test_token(token: str = Depends(check_token)):
    return {"email": token}


@router.get("/user/{user_id}", response_model=PublicUser)
async def get_user_account(user_id: str) -> PublicUser:
    if len(user_id) == 24:
        user = await get_user_from_id(user_id)
    else:
        user = await get_user_from_username(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return PublicUser(**user.dict())


@router.get("/users/verify/{key}")
async def get_verify_code(key: str):
    res = await col("users").find_one_and_update({"verified": key}, {"$set": {"verified": True}})
    if res is not None:
        return RedirectResponse(settings.root_address, 306)
    else:
        return PlainTextResponse("Wrong Code!", 404)
