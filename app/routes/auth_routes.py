from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, EmailStr
from uuid import uuid4
from datetime import datetime, timezone
import hashlib
from app.core.database import supabase  # ✅ On reste connecté à Supabase

router = APIRouter()

# -----------------------------
# 🔹 1. Modèle d'inscription
# -----------------------------
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# -----------------------------
# 🔹 2. Route POST /signup
# -----------------------------
@router.post("/signup")
def signup(data: SignupRequest):
    # Vérifie si le username ou l'email existe déjà
    existing = supabase.table("users").select("id").or_(
        f"username.eq.{data.username},email.eq.{data.email}"
    ).execute()

    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nom d'utilisateur ou email déjà utilisé."
        )

    # Hash du mot de passe
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()

    # Token de confirmation
    confirmation_token = str(uuid4())

    # Insertion dans Supabase
    response = supabase.table("users").insert({
        "id": str(uuid4()),
        "username": data.username,
        "email": data.email,
        "password": hashed_password,
        "role": "utilisateur",         # rôle neutre par défaut
        "active": False,               # désactivé tant qu’un admin ne valide pas
        "email_confirmed": False,
        "confirmation_token": confirmation_token,
        "created_at": datetime.now(timezone.utc)
    }).execute()

    if response.error:
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription.")

    # Affiche le lien de confirmation (à remplacer plus tard par un vrai email)
    print(f"🔗 Lien de confirmation à envoyer : /confirm-email/{confirmation_token}")

    return {"message": "Utilisateur créé. Vérifiez votre email pour confirmer le compte."}


# -----------------------------
# 🔹 3. Route GET /confirm-email/{token}
# -----------------------------
@router.get("/confirm-email/{token}")
def confirm_email(token: str):
    # Vérifie si un utilisateur avec ce token existe
    response = supabase.table("users").select("*").eq("confirmation_token", token).execute()

    if not response.data or len(response.data) == 0:
        raise HTTPException(status_code=404, detail="Token invalide ou déjà utilisé.")

    user = response.data[0]

    # Met à jour les champs dans la table
    update_response = supabase.table("users").update({
        "email_confirmed": True,
        "active": True,
        "confirmation_token": None,
        "last_login": datetime.now(timezone.utc)
    }).eq("id", user["id"]).execute()

    if update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erreur lors de la validation de l'email.")

    return {"message": "✅ Adresse email confirmée. Vous pouvez maintenant vous connecter."}


# -----------------------------
# 🔹 4. Route POST /login
# -----------------------------
@router.post("/login")
async def login(request: Request):
    data = await request.json()
    login_input = data.get("login")  # peut être un email OU un username
    password = data.get("password")

    if not login_input or not password:
        raise HTTPException(status_code=400, detail="Champs manquants.")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Vérifie login + password + statut actif
    response = supabase.table("users") \
        .select("*") \
        .or_(f"username.eq.{login_input},email.eq.{login_input}") \
        .eq("password", hashed_password) \
        .eq("active", True) \
        .eq("email_confirmed", True) \
        .execute()

    if not response.data or len(response.data) == 0:
        raise HTTPException(status_code=401, detail="Identifiants invalides ou compte inactif.")

    user = response.data[0]

    # Met à jour le champ last_login
    supabase.table("users").update({
        "last_login": datetime.now(timezone.utc)
    }).eq("id", user["id"]).execute()

    return {
        "message": "✅ Connexion réussie.",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }
