from typing import Optional, List

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


class BaseFile(BaseModel):
    creation_date: str
    user_id: str
    hashsum: str
    file_id: str
    reported: bool = False


class BaseInputThing(BaseModel):
    description: str
    title: str
    file: str
    pictures: List[str]


class BaseThing(BaseInputThing):
    creation_date: str
    id: str
    user_id: str
