from fastapi import FastAPI
from app.core.database import test_connection

app = FastAPI()

@app.on_event("startup")
def startup():
    test_connection()

@app.get("/")
def root():
    return {"message": "API FastAPI opérationnelle"}
