from helpers.models import *
from helpers.config import settings, col

from typing import List, Union


async def search_thing(query: str, limit: int, category: str = "all") -> Union[List[PublicThing], None]:
    if category == "all":
        res = col("things").find({"$text": {"$search": query}}, {"_id": 0})
    else:
        res = col("things").find({"$text": {"$search": query}, "category": category}, {"_id": 0})

    return [PublicThing(**r) async for r in res]
