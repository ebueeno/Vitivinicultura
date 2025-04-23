from fastapi import FastAPI
from routers import importacao

app = FastAPI()

app.include_router(importacao.router, tags=["importacao"])


@app.get("/")
def home():
    return {"message": "API está rodando"}
