# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from pymongo import MongoClient
# from bson import ObjectId
# import os

# app = FastAPI()

# client = MongoClient("mongodb://localhost:27017")
# db = client["chat_db"]
# collection = db["history"]

# class HistoryEntry(BaseModel):
#     chat_id: str
#     query: str
#     response: str

# @app.post("/history")
# def add_history(entry: HistoryEntry):
#     collection.insert_one(entry.dict())
#     return {"status": "stored"}

# @app.get("/history/{chat_id}")
# def get_history(chat_id: str):
#     entries = list(collection.find({"chat_id": chat_id}, {"_id": 0}))
#     if not entries:
#         raise HTTPException(status_code=404, detail="No history found")
#     return {"chat_id": chat_id, "history": entries}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["chat_db"]
collection = db["history"]

# -------- Data Model -------- #
class HistoryEntry(BaseModel):
    chat_id: str
    query: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------- Save History -------- #
@app.post("/history")
def add_history(entry: HistoryEntry):
    collection.insert_one(entry.dict())
    return {"status": "stored", "chat_id": entry.chat_id}

# -------- Get History by Chat ID -------- #
@app.get("/history/{chat_id}")
def get_history(chat_id: str):
    entries = list(collection.find({"chat_id": chat_id}, {"_id": 0}))
    if not entries:
        raise HTTPException(status_code=404, detail="No history found")
    return {"chat_id": chat_id, "history": entries}
