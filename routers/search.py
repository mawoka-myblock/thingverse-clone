import hashlib
import json
import uuid
from typing import Union
from datetime import datetime, timedelta
import os
import re
import typesense
import io

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from fastapi.responses import RedirectResponse, PlainTextResponse, JSONResponse
from helpers.config import settings, col, minio
from helpers.models import *
import zipfile
from helpers.security.verify import send_mail
from helpers.security.auth import get_current_user, get_password_hash, get_user_from_id, verify_password, \
    create_access_token, get_user_from_mail, get_user_from_username, authenticate_user
from helpers.search import search_thing
import fuzzy

router = APIRouter()
"""
for word in terms:
    if len(word) <= 2 or word in stop_words:
        # Skip short words or ignorable words
        continue
    fuzzy_terms = []
    fuzzy_terms.append(dmeta(word)[0]) # doblemetaphone
    fuzzy_terms.append(fuzzy.nysiis(word)) # NYSIIS
    for term in fuzzy_terms:
        search_terms_collection.insert({
            "keyword": term,
            "original": word,
            "item": item["_id"]
        })
"""


@router.get("/things")
async def thing_search(query: str, limit: Optional[int] = 10, category: Optional[str] = "*",
                       page: Optional[int] = 1, query_by: str = "title"):
    client = typesense.Client({
        'api_key': settings.typesense_api_key,
        "nodes": [{
            "host": settings.typesense_host,
            "port": settings.typesense_port,
            "protocol": settings.typesense_protocol
        }],
        "connection_timeout_seconds": settings.typesense_timeout
    })
    search_params = {
        "q": query,
        "query_by": query_by,
        "page": page,
        "per_page": limit,
        #"filter_by": f'category: {category}'
    }

    return client.collections["things"].documents.search(search_params)
