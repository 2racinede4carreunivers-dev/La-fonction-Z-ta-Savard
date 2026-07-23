"""
Module d'authentification par email pour L'Univers est au Carré.

Système de vérification par code à 6 chiffres envoyé par email.
Les codes expirent après 60 minutes.

Admin: philippotcarre@outlook.com (accès à l'historique des questions)
Contact: Thomasphilippesavard@gmail.com
"""
import os
import random
import string
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
import resend
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configuration
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "onboarding@resend.dev")
ADMIN_EMAIL = "philippotcarre@outlook.com"
ADMIN_CONTACT_EMAIL = "Thomasphilippesavard@gmail.com"
CODE_EXPIRY_MINUTES = 60

# Initialize Resend
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


class EmailVerificationRequest(BaseModel):
    email: EmailStr


class CodeVerificationRequest(BaseModel):
    email: EmailStr
    code: str


class UserSession(BaseModel):
    email: str
    verified: bool = False
    is_admin: bool = False
    created_at: datetime
    last_activity: datetime


# In-memory store for pending verifications (in production, use Redis/MongoDB)
pending_verifications: dict[str, dict] = {}
# Active user sessions
active_sessions: dict[str, UserSession] = {}


def generate_verification_code() -> str:
    """Génère un code de vérification à 6 chiffres."""
    return ''.join(random.choices(string.digits, k=6))


def is_admin(email: str) -> bool:
    """Vérifie si l'email est celui de l'administrateur."""
    return email.lower() == ADMIN_EMAIL.lower()


async def send_verification_email(email: str, code: str) -> dict:
    """Envoie un email de vérification avec le code à 6 chiffres."""
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not configured - email not sent")
        return {"status": "mock", "message": "Email service not configured", "code": code}
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background-color: #1a1a2e; padding: 30px; border-radius: 10px; text-align: center;">
            <h1 style="color: #ffd700; margin: 0 0 10px 0;">L'Univers est au Carré</h1>
            <p style="color: #ffffff; margin: 0;">Géométrie du Spectre des Nombres Premiers</p>
        </div>
        
        <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; margin-top: 20px;">
            <h2 style="color: #1a1a2e; margin-top: 0;">Vérification de votre adresse email</h2>
            
            <p style="color: #333333; line-height: 1.6;">
                Bonjour,<br><br>
                Vous avez demandé l'accès à l'application <strong>L'Univers est au Carré</strong>.
                Voici votre code de vérification :
            </p>
            
            <div style="background-color: #1a1a2e; padding: 20px; border-radius: 8px; text-align: center; margin: 25px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #ffd700; letter-spacing: 8px;">{code}</span>
            </div>
            
            <p style="color: #666666; font-size: 14px;">
                Ce code est valide pendant <strong>60 minutes</strong>.<br>
                Si vous n'avez pas demandé ce code, ignorez simplement cet email.
            </p>
        </div>
        
        <div style="text-align: center; padding: 20px; color: #666666; font-size: 12px;">
            <p>© Philippe Thomas Savard & E1 (Emergent Labs)</p>
            <p>www.universestaucarre.com</p>
        </div>
    </body>
    </html>
    """
    
    params = {
        "from": SENDER_EMAIL,
        "to": [email],
        "subject": "🔐 Code de vérification - L'Univers est au Carré",
        "html": html_content
    }
    
    try:
        email_response = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Verification email sent to {email}")
        return {
            "status": "success",
            "message": f"Code envoyé à {email}",
            "email_id": email_response.get("id") if isinstance(email_response, dict) else str(email_response)
        }
    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")
        return {"status": "error", "message": str(e)}


async def initiate_verification(email: str) -> dict:
    """Initie le processus de vérification par email."""
    code = generate_verification_code()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=CODE_EXPIRY_MINUTES)
    
    # Store pending verification
    pending_verifications[email.lower()] = {
        "code": code,
        "expiry": expiry,
        "attempts": 0
    }
    
    # Send email
    result = await send_verification_email(email, code)
    
    return {
        "success": result["status"] in ["success", "mock"],
        "message": f"Un code de vérification a été envoyé à {email}. Il expire dans 60 minutes.",
        "expires_in_minutes": CODE_EXPIRY_MINUTES,
        "email_status": result["status"]
    }


def verify_code(email: str, code: str) -> dict:
    """Vérifie le code entré par l'utilisateur."""
    email_lower = email.lower()
    
    if email_lower not in pending_verifications:
        return {
            "success": False,
            "message": "Aucune demande de vérification en cours pour cet email. Veuillez recommencer."
        }
    
    verification = pending_verifications[email_lower]
    
    # Check expiry
    if datetime.now(timezone.utc) > verification["expiry"]:
        del pending_verifications[email_lower]
        return {
            "success": False,
            "message": "Le code a expiré. Veuillez demander un nouveau code."
        }
    
    # Check attempts (max 5)
    if verification["attempts"] >= 5:
        del pending_verifications[email_lower]
        return {
            "success": False,
            "message": "Trop de tentatives. Veuillez demander un nouveau code."
        }
    
    verification["attempts"] += 1
    
    # Verify code
    if verification["code"] != code:
        remaining = 5 - verification["attempts"]
        return {
            "success": False,
            "message": f"Code incorrect. {remaining} tentative(s) restante(s)."
        }
    
    # Success - create session
    del pending_verifications[email_lower]
    
    session_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    now = datetime.now(timezone.utc)
    
    active_sessions[session_token] = UserSession(
        email=email_lower,
        verified=True,
        is_admin=is_admin(email_lower),
        created_at=now,
        last_activity=now
    )
    
    return {
        "success": True,
        "message": "Vérification réussie ! Bienvenue sur L'Univers est au Carré.",
        "session_token": session_token,
        "is_admin": is_admin(email_lower),
        "email": email_lower
    }


def validate_session(session_token: str) -> Optional[UserSession]:
    """Valide un token de session et retourne les infos utilisateur."""
    if session_token not in active_sessions:
        return None
    
    session = active_sessions[session_token]
    
    # Update last activity
    session.last_activity = datetime.now(timezone.utc)
    
    # Sessions expire after 24 hours of inactivity
    if datetime.now(timezone.utc) - session.last_activity > timedelta(hours=24):
        del active_sessions[session_token]
        return None
    
    return session


def logout(session_token: str) -> bool:
    """Déconnecte l'utilisateur."""
    if session_token in active_sessions:
        del active_sessions[session_token]
        return True
    return False


# Export functions
__all__ = [
    "initiate_verification",
    "verify_code",
    "validate_session",
    "logout",
    "is_admin",
    "ADMIN_EMAIL",
    "ADMIN_CONTACT_EMAIL",
    "EmailVerificationRequest",
    "CodeVerificationRequest",
    "UserSession"
]
