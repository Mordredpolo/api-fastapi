import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d’environnement depuis le fichier .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_connection() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Les variables SUPABASE_URL ou SUPABASE_KEY ne sont pas définies dans .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Instance globale utilisée dans toutes les routes
supabase = get_connection()
