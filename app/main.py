from fastapi import FastAPI
from app.core.database import test_connection  # ✅ Corrigé ici

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    test_connection()  # ✅ Corrigé ici

@app.get("/")
def read_root():
    return {"message": "API FastAPI opérationnelle"}

# ✅ Route pour ping Render régulièrement
@app.get("/ping")
def ping():
    return {"status": "ok"}
