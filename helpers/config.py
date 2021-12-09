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
    mongo_db: str = "thingverse"
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

license_dict = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC-BY": "https://creativecommons.org/licenses/by/4.0/",
    "CC-BY-SA": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC-BY-ND": "https://creativecommons.org/licenses/by-nd/4.0/",
    "CC-BY-NC": "https://creativecommons.org/licenses/by-nc/4.0/",
    "CC-BY-NC-SA": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "CC-BY-NC-ND": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
    "CC-BY-NC-SA-ND": "https://creativecommons.org/licenses/by-nc-sa-nd/4.0/",
    "GPL": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    "MIT": "https://opensource.org/licenses/MIT",
    "BSD": "https://opensource.org/licenses/BSD-3-Clause",
    "LGPL": "https://www.gnu.org/licenses/lgpl-3.0.en.html",
}

minio = Minio(
    endpoint=settings.minio_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)
