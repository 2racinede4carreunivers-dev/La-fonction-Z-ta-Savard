"""
Module de gestion de l'historique et des suggestions pour L'Univers est au Carré.

- Historique des questions posées aux IA (accessible par l'admin)
- Suggestions des utilisateurs (max 350 caractères)
"""
import os
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "univers_carre")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
questions_history = db["questions_history"]
user_suggestions = db["user_suggestions"]
user_accounts = db["user_accounts"]


class QuestionRecord(BaseModel):
    """Enregistrement d'une question posée à une IA."""
    user_email: str
    ia_module: str  # gabriel, specialisee, evolutive, socratique
    question: str
    response_preview: str = ""  # First 200 chars of response
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserSuggestion(BaseModel):
    """Suggestion d'un utilisateur (max 350 caractères)."""
    user_email: str
    suggestion: str = Field(..., max_length=350)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserAccount(BaseModel):
    """Compte utilisateur enregistré."""
    email: str
    first_visit: datetime
    last_visit: datetime
    total_visits: int = 1
    total_questions: int = 0


def record_question(user_email: str, ia_module: str, question: str, response: str = "") -> str:
    """Enregistre une question posée à une IA."""
    record = {
        "user_email": user_email.lower(),
        "ia_module": ia_module,
        "question": question,
        "response_preview": response[:200] if response else "",
        "timestamp": datetime.now(timezone.utc)
    }
    
    result = questions_history.insert_one(record)
    
    # Update user stats
    user_accounts.update_one(
        {"email": user_email.lower()},
        {"$inc": {"total_questions": 1}},
        upsert=False
    )
    
    return str(result.inserted_id)


def get_questions_history(
    limit: int = 100,
    user_email: Optional[str] = None,
    ia_module: Optional[str] = None
) -> List[dict]:
    """Récupère l'historique des questions (admin only)."""
    query = {}
    if user_email:
        query["user_email"] = user_email.lower()
    if ia_module:
        query["ia_module"] = ia_module
    
    cursor = questions_history.find(
        query,
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    
    return list(cursor)


def submit_suggestion(user_email: str, suggestion: str) -> dict:
    """Soumet une suggestion (max 350 caractères)."""
    if len(suggestion) > 350:
        return {
            "success": False,
            "message": "La suggestion ne doit pas dépasser 350 caractères."
        }
    
    if len(suggestion.strip()) < 10:
        return {
            "success": False,
            "message": "La suggestion doit contenir au moins 10 caractères."
        }
    
    record = {
        "user_email": user_email.lower(),
        "suggestion": suggestion.strip(),
        "timestamp": datetime.now(timezone.utc)
    }
    
    user_suggestions.insert_one(record)
    
    return {
        "success": True,
        "message": "Merci pour votre suggestion ! Elle sera examinée par l'administrateur."
    }


def get_all_suggestions(limit: int = 100) -> List[dict]:
    """Récupère toutes les suggestions (admin only)."""
    cursor = user_suggestions.find(
        {},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    
    return list(cursor)


def register_user_visit(email: str) -> dict:
    """Enregistre ou met à jour la visite d'un utilisateur."""
    now = datetime.now(timezone.utc)
    email_lower = email.lower()
    
    existing = user_accounts.find_one({"email": email_lower}, {"_id": 0})
    
    if existing:
        user_accounts.update_one(
            {"email": email_lower},
            {
                "$set": {"last_visit": now},
                "$inc": {"total_visits": 1}
            }
        )
        return {
            "is_new": False,
            "email": email_lower,
            "total_visits": existing.get("total_visits", 0) + 1
        }
    else:
        user_accounts.insert_one({
            "email": email_lower,
            "first_visit": now,
            "last_visit": now,
            "total_visits": 1,
            "total_questions": 0
        })
        return {
            "is_new": True,
            "email": email_lower,
            "total_visits": 1
        }


def get_all_users(limit: int = 100) -> List[dict]:
    """Récupère tous les utilisateurs (admin only)."""
    cursor = user_accounts.find(
        {},
        {"_id": 0}
    ).sort("last_visit", -1).limit(limit)
    
    return list(cursor)


def get_user_stats() -> dict:
    """Statistiques globales (admin only)."""
    total_users = user_accounts.count_documents({})
    total_questions = questions_history.count_documents({})
    total_suggestions = user_suggestions.count_documents({})
    
    # Questions par module IA
    pipeline = [
        {"$group": {"_id": "$ia_module", "count": {"$sum": 1}}}
    ]
    questions_by_module = {doc["_id"]: doc["count"] for doc in questions_history.aggregate(pipeline)}
    
    return {
        "total_users": total_users,
        "total_questions": total_questions,
        "total_suggestions": total_suggestions,
        "questions_by_module": questions_by_module
    }


__all__ = [
    "record_question",
    "get_questions_history",
    "submit_suggestion",
    "get_all_suggestions",
    "register_user_visit",
    "get_all_users",
    "get_user_stats",
    "QuestionRecord",
    "UserSuggestion",
    "UserAccount"
]
