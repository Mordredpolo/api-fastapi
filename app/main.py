from fastapi import FastAPI
from app.routes import auth_routes  # ✅ Import du router pour les routes d'authentification

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API FastAPI opérationnelle"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

# ✅ Inclusion des routes d'authentification
app.include_router(auth_routes.router)