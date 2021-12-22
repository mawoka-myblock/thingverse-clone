from typing import Optional, List
from bson import ObjectId
from pydantic import Field
from pydantic import BaseModel as PydanticBaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class BaseUserCreate(BaseModel):
    email: str
    password: str
    username: str


class PublicUser(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    public_collections: List[str] = []
    username: str
    date_joined: str


class PrivateUser(PublicUser):
    private_collections: List[str] = []
    email: str


class UserInDB(BaseUserCreate):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    public_collections: List[str] = []
    private_collections: List[str] = []
    verified: bool = False
    things_created: int = 0
    is_superuser: bool = False
    date_joined: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class BaseFile(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    creation_date: str
    user_id: PyObjectId
    hash: str
    reported: bool = False


class BaseInputThing(BaseModel):
    category: str
    description: str
    file: str
    title: str
    pictures: Optional[List[str]] = []
    license: str


class PublicThing(BaseInputThing):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    comment_count: int = 0
    like_count: int = 0
    make_count: int = 0
    remixes: int = 0
    creation_date: str
    file: str
    user_id: PyObjectId
    downloads: int = 0


class BaseThing(PublicThing):
    hash: str
