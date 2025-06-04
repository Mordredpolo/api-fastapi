import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Fonction optionnelle pour tester que la connexion fonctionne
def test_supabase_connection():
    try:
        response = supabase.table("users").select("id").limit(1).execute()
        print("✅ Connexion à Supabase réussie.")
    except Exception as e:
        print("❌ Erreur de connexion à Supabase :", e)
