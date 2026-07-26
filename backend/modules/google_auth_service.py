"""
Module d'authentification Google OAuth pour L'Univers est au Carré.

Utilise Emergent Auth pour une authentification simplifiée via Google.
Admin: philippotcarre@outlook.com
Contact: Thomasphilippesavard@gmail.com
"""
import os
import uuid
import httpx
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "univers_carre")
ADMIN_EMAIL = "philippotcarre@outlook.com"
ADMIN_CONTACT_EMAIL = "Thomasphilippesavard@gmail.com"
SESSION_EXPIRY_DAYS = 7

# Emergent Auth endpoint
EMERGENT_AUTH_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

# MongoDB connection
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db["users"]
sessions_collection = db["user_sessions"]


class UserSession(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    is_admin: bool = False


class UserData(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    is_admin: bool = False
    created_at: datetime
    last_login: datetime


def is_admin(email: str) -> bool:
    """Vérifie si l'email est celui de l'administrateur."""
    return email.lower() == ADMIN_EMAIL.lower()


async def exchange_session_id(session_id: str) -> Optional[dict]:
    """
    Échange le session_id temporaire contre les données utilisateur.
    Appelle l'endpoint Emergent Auth.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                EMERGENT_AUTH_SESSION_URL,
                headers={"X-Session-ID": session_id},
                timeout=10.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Emergent Auth error: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        logger.error(f"Error exchanging session_id: {e}")
        return None


def create_or_update_user(email: str, name: str, picture: Optional[str] = None) -> str:
    """
    Crée ou met à jour un utilisateur dans la base de données.
    Retourne le user_id.
    """
    email_lower = email.lower()
    now = datetime.now(timezone.utc)
    
    existing_user = users_collection.find_one({"email": email_lower}, {"_id": 0})
    
    if existing_user:
        # Update existing user
        users_collection.update_one(
            {"email": email_lower},
            {
                "$set": {
                    "name": name,
                    "picture": picture,
                    "last_login": now
                }
            }
        )
        return existing_user["user_id"]
    else:
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        users_collection.insert_one({
            "user_id": user_id,
            "email": email_lower,
            "name": name,
            "picture": picture,
            "is_admin": is_admin(email_lower),
            "created_at": now,
            "last_login": now,
            "total_visits": 1,
            "total_questions": 0
        })
        return user_id


def create_session(user_id: str, session_token: str) -> dict:
    """
    Crée une nouvelle session pour l'utilisateur.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=SESSION_EXPIRY_DAYS)
    
    # Remove any existing sessions for this user
    sessions_collection.delete_many({"user_id": user_id})
    
    # Create new session
    sessions_collection.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "created_at": now
    })
    
    return {
        "session_token": session_token,
        "expires_at": expires_at.isoformat()
    }


def validate_session(session_token: str) -> Optional[UserSession]:
    """
    Valide un token de session et retourne les infos utilisateur.
    """
    if not session_token:
        return None
    
    # Find session
    session_doc = sessions_collection.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session_doc:
        return None
    
    # Check expiry
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        # Session expired, delete it
        sessions_collection.delete_one({"session_token": session_token})
        return None
    
    # Get user data
    user_doc = users_collection.find_one(
        {"user_id": session_doc["user_id"]},
        {"_id": 0}
    )
    
    if not user_doc:
        return None
    
    # Update last activity
    users_collection.update_one(
        {"user_id": user_doc["user_id"]},
        {"$set": {"last_login": datetime.now(timezone.utc)}}
    )
    
    return UserSession(
        user_id=user_doc["user_id"],
        email=user_doc["email"],
        name=user_doc["name"],
        picture=user_doc.get("picture"),
        is_admin=user_doc.get("is_admin", is_admin(user_doc["email"]))
    )


def delete_session(session_token: str) -> bool:
    """
    Supprime une session (déconnexion).
    """
    result = sessions_collection.delete_one({"session_token": session_token})
    return result.deleted_count > 0


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Récupère un utilisateur par son email.
    """
    return users_collection.find_one(
        {"email": email.lower()},
        {"_id": 0}
    )


def increment_user_questions(user_id: str) -> None:
    """
    Incrémente le compteur de questions d'un utilisateur.
    """
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"total_questions": 1}}
    )


__all__ = [
    "exchange_session_id",
    "create_or_update_user",
    "create_session",
    "validate_session",
    "delete_session",
    "get_user_by_email",
    "increment_user_questions",
    "is_admin",
    "ADMIN_EMAIL",
    "ADMIN_CONTACT_EMAIL",
    "UserSession",
    "UserData"
]
