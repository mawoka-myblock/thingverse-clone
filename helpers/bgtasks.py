import json

from celery import Celery
from celery.utils.log import get_task_logger
from helpers.config import settings, col
import pymongo.errors
import typesense
from bson import json_util

# Create the celery app and get the logger
celery_app = Celery('tasks', broker=settings.redis)
logger = get_task_logger(__name__)


@celery_app.task
async def copy_to_typesense():
    print('Running typesense task')
    client = typesense.Client({
        'api_key': settings.typesense_api_key,
        "nodes": [{
            "host": settings.typesense_host,
            "port": settings.typesense_port,
            "protocol": settings.typesense_protocol
        }],
        "connection_timeout_seconds": settings.typesense_timeout
    })
    try:
        client.collections['things'].delete()
    except Exception as e:
        pass
    db_schema = {  # MUST FIT BASETHING IN helpers.models!!!
        "name": "things",
        "fields": [
            {"name": "category", "type": "string"},
            {"name": "description", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "like_count", "type": "int32"},
            {"name": "category", "type": "string"},

        ],
        "default_sorting_field": "like_count",
    }
    create_collection_response = client.collections.create(db_schema)
    resume_token = None
    pipeline = [{'$match': {'operationType': '*'}}]
    try:
        async with col("things").watch() as stream:
            print("Starting stream")
            async for insert_change in stream:
                print("\n", insert_change, "\n", insert_change["operationType"])
                if insert_change['operationType'] == 'delete':
                    client.collections['things'].documents[str(insert_change['documentKey']['_id'])].delete()
                elif insert_change["operationType"] == "update":
                    data = json.dumps(insert_change['updateDescription']["updatedFields"], default=json_util.default)
                    client.collections['things'].documents[str(insert_change['documentKey']['_id'])].update(data)
                else:
                    insert_change['fullDocument']['id'] = str(insert_change['fullDocument']['_id'])
                    del insert_change['fullDocument']['_id']
                    data = json.dumps(insert_change['fullDocument'], default=json_util.default)
                    print("\n", data)
                    client.collections["things"].documents.upsert(data)
                resume_token = stream.resume_token
    except pymongo.errors.PyMongoError:
        print("Error1")
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        if resume_token is None:
            # There is no usable resume token because there was a
            # failure during ChangeStream initialization.
            print("error!")
        else:
            # Use the interrupted ChangeStream's resume token to
            # create a new ChangeStream. The new stream will
            # continue from the last seen insert change without
            # missing any events.
            async with col("things").watch(
                    pipeline, resume_after=resume_token) as stream:
                async for insert_change in stream:
                    print(insert_change)


async def migrate_existing():
    print('Running typesense task')
    client = typesense.Client({
        'api_key': settings.typesense_api_key,
        "nodes": [{
            "host": settings.typesense_host,
            "port": settings.typesense_port,
            "protocol": settings.typesense_protocol
        }],
        "connection_timeout_seconds": settings.typesense_timeout
    })
    try:
        client.collections['things'].delete()
    except Exception as e:
        pass
    db_schema = {  # MUST FIT BASETHING IN helpers.models!!!
        "name": "things",
        "fields": [
            {"name": "category", "type": "string"},
            {"name": "description", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "like_count", "type": "int32"},
            {"name": "category", "type": "string"},

        ],
        "default_sorting_field": "like_count",
    }
    create_collection_response = client.collections.create(db_schema)
    resume_token = None
    pipeline = [{'$match': {'operationType': '*'}}]
    print("Starting stream")
    async for document in col("things").find({}):
        document['id'] = str(document['_id'])
        del document['_id']
        data = json.dumps(document, default=json_util.default)
        print("\n", data)
        client.collections["things"].documents.upsert(data)

