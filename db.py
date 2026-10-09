import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).parent / ".env", override=True)

_uri = os.getenv("MONGO_URI")
_collection = None
if _uri:
    _client = MongoClient(_uri, serverSelectionTimeoutMS=3000)
    _collection = _client[os.getenv("MONGO_DB", "ragbot")]["queries"]


def log_query(question, answer):
    if _collection is None:
        return
    try:
        _collection.insert_one({
            "question": question,
            "answer": answer,
            "created_at": datetime.now(timezone.utc),
        })
    except Exception as e:
        print("Mongo log failed:", e)


def recent_queries(limit=10):
    if _collection is None:
        return []
    docs = _collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
    return list(docs)