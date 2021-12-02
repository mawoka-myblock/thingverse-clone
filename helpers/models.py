from typing import Optional, List

from pydantic import BaseModel


class BaseUserCreate(BaseModel):
    email: str
    password: str
    username: str


class PublicUser(BaseModel):
    public_collections: List[str] = []
    username: str
    id: str
    date_joined: str


class PrivateUser(PublicUser):
    private_collections: List[str] = []
    email: str


class UserInDB(BaseUserCreate):
    public_collections: List[str] = []
    private_collections: List[str] = []
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
    hash: str
    file_id: str
    reported: bool = False


class BaseInputThing(BaseModel):
    category: str
    description: str
    file: str
    title: str
    pictures: Optional[List[str]] = []
    license: str


class PublicThing(BaseInputThing):
    comment_count: int = 0
    like_count: int = 0
    make_count: int = 0
    remixes: int = 0
    creation_date: str
    id: str
    file: str
    user_id: str
    downloads: int = 0


class BaseThing(PublicThing):
    hash: str

