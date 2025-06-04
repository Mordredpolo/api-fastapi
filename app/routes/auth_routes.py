from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.database import supabase
from datetime import datetime, timezone
from uuid import uuid4
import bcrypt
import secrets

router = APIRouter()

# ✅ Schéma de données pour l'inscription
class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

@router.post("/register")
def register_user(data: RegisterRequest):
    # Vérifier si l'email ou le username existe déjà
    existing = supabase.table("users").select("id").or_(
        f"email.eq.{data.email},username.eq.{data.username}"
    ).execute()

    if existing.data:
        raise HTTPException(status_code=400, detail="Email ou nom d'utilisateur déjà utilisé")

    # ✅ Hash du mot de passe
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # ✅ Token de confirmation aléatoire
    confirmation_token = secrets.token_urlsafe(32)

    # ✅ Insertion dans la table
    response = supabase.table("users").insert({
        "id": str(uuid4()),
        "email": data.email,
        "username": data.username,
        "password": hashed_password,
        "role": "employé",
        "active": False,
        "email_confirmed": False,
        "confirmation_token": confirmation_token,
        "created_at": datetime.now(timezone.utc).isoformat()
    }).execute()

    if response.error:
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")

    # Simuler l’envoi de l’email de confirmation (à remplacer par un vrai service plus tard)
    print(f"[SIMULATION] Email de confirmation envoyé à {data.email} avec le lien :")
    print(f"https://ton-domaine.com/confirm?token={confirmation_token}")

    return {"message": "Inscription réussie. Vérifiez votre email pour confirmer votre compte."}
