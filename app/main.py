from fastapi import FastAPI
from app.core.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "API FastAPI opérationnelle"}

# ✅ Route pour éviter que Render mette l'API en veille
@app.get("/ping")
def ping():
    return {"status": "ok"}
