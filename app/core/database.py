import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DB_URL")

engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        print("✅ Connexion à la base réussie.")
    except Exception as e:
        print("❌ Erreur de connexion à la base :", e)
