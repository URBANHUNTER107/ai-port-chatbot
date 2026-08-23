import os
from datetime import datetime, timezone
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
db = client["farhanAI"]
messages = db["messages"]


def save_message(visitor_id, name, question, answer):
    try:
        messages.insert_one({
            "visitor_id": visitor_id,
            "name": name,
            "question": question,
            "answer": answer,
            "created_at": datetime.now(timezone.utc)
        })
    except Exception as error:
        print("MongoDB save failed:", error)


def get_history(visitor_id):
    try:
        docs = messages.find({"visitor_id": visitor_id}).sort("created_at", 1)
        return [
            {
                "name": d.get("name"),
                "question": d.get("question"),
                "answer": d.get("answer")
            }
            for d in docs
        ]
    except Exception as error:
        print("MongoDB fetch failed:", error)
        return []