from pydantic import BaseSettings, RedisDsn
from pymongo.collection import Collection
import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from minio import Minio


def col(column: str) -> Collection:
    return AsyncIOMotorClient(settings.mongo_url)[settings.mongo_db][column]


def redis() -> aioredis.client.Redis:
    aioredis.decode_responses = True
    return aioredis.from_url(settings.redis, encoding="utf-8")


class Settings(BaseSettings):
    """
    Settings class for the shop app.
    """
    root_address: str = "http://127.0.0.1:8000"
    redis: RedisDsn = "redis://localhost:6379/0"
    skip_email_verification: bool = False
    mongo_url: str
    mongo_db: str = "thingiverse"
    mail_address: str
    mail_password: str
    mail_username: str
    mail_server: str
    mail_port: int
    secret_key: str
    minio_url: str = "127.0.0.1"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool = True
    access_token_expire_minutes: int = 30
    cache_expiry: int = 86400

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

minio = Minio(
    endpoint=settings.minio_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)
