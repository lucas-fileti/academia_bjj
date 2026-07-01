from fastapi import FastAPI
from database import Base, engine

from models.aluno_model import Aluno
from models.mensalidade_model import Mensalidade

from routers.aluno_router import router as aluno_router
from routers.mensalidade_router import router as mensalidade_router
from routers.dashboard_router import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gerenciamento BJJ",
    description="API para gerenciamento de academia de Jiu-Jitsu",
    version="1.0.0"
)

app.include_router(aluno_router)
app.include_router(mensalidade_router)
app.include_router(dashboard_router)

@app.get("/")
def home():
    return {
        "message": "Bem-vindo à API de Gerenciamento de Academia de Jiu-Jitsu!"
    }