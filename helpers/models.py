from pydantic import BaseModel

from typing import Optional

from pydantic import BaseModel


class BaseUserCreate(BaseModel):
    email: str
    password: str
    username: str


class PublicUser(BaseModel):
    username: str
    id: str
    date_joined: str


class UserInDB(BaseUserCreate):
    verified: bool = False
    things_created: int = 0
    id: str
    is_superuser: bool = False
    date_joined: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
