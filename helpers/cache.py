from bson import ObjectId

from helpers.config import redis, col
from rapidjson import loads
from typing import Union
from helpers.config import settings
from helpers.models import UserInDB


async def cache_account(criteria: str, content: str) -> Union[UserInDB, None]:
    async def insert_into_redis(usermodel: UserInDB, key: str):
        await redis().set(key, usermodel.json(), ex=settings.cache_expiry)

    if criteria == "email":
        res = await col("users").find_one({"email": content, "verified": True})
        if res is None:
            return None
        user = UserInDB.parse_obj(res)
        await insert_into_redis(user, content)
        return user
    elif criteria == "username":
        res = await col("users").find_one({"username": content, "verified": True})
        if res is None:
            return None
        user = UserInDB.parse_obj(res)
        await insert_into_redis(user, content)
        return user
    elif criteria == "id":
        res = await col("users").find_one({"_id": ObjectId(content), "verified": True})
        if res is None:
            return None
        user = UserInDB.parse_obj(res)
        await insert_into_redis(user, content)
        return user
    else:
        return None


async def get_from_redis(key: str) -> Union[None, UserInDB]:
    user = await redis().get(key)
    if user is None:
        return None
    else:
        return UserInDB.parse_obj(loads(user.decode()))


async def get_cache(criteria: str, content: str) -> UserInDB:
    cache = await get_from_redis(content)
    if cache is not None:
        return cache
    else:
        return await cache_account(criteria, content)
