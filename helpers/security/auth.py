from helpers.config import settings, col
from helpers.models import *
from typing import Union
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from helpers.cache import get_cache
from fastapi import APIRouter, Depends, HTTPException, status
import pydantic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user_from_mail(email: str) -> Union[UserInDB, None]:
    return await get_cache(criteria="email", content=email)


async def get_user_from_username(username: str) -> Union[UserInDB, None]:
    return await get_cache(criteria="username", content=username)


async def get_user_from_id(id: str) -> Union[UserInDB, None]:
    return await get_cache(criteria="id", content=id)


async def authenticate_user(email: str, password: str) -> Union[UserInDB, bool]:
    user = await get_user_from_mail(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user_from_mail(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
