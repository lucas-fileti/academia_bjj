from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.aluno_model import Aluno
from models.mensalidade_model import Mensalidade
from routers.mensalidade_router import atualizar_mensalidades_vencidas


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/resumo")
def resumo_dashboard(db: Session = Depends(get_db)):
    atualizar_mensalidades_vencidas(db)

    total_alunos_ativos = db.query(Aluno).filter(
        Aluno.ativo == True
    ).count()

    mensalidades_pendentes = db.query(Mensalidade).filter(
        Mensalidade.status == "pendente"
    ).count()

    mensalidades_vencidas = db.query(Mensalidade).filter(
        Mensalidade.status == "vencida"
    ).count()

    mensalidades_pagas = db.query(Mensalidade).filter(
        Mensalidade.status == "paga"
    ).count()

    valor_recebido = db.query(func.sum(Mensalidade.valor)).filter(
        Mensalidade.status == "paga"
    ).scalar()

    valor_vencido = db.query(func.sum(Mensalidade.valor)).filter(
        Mensalidade.status == "vencida"
    ).scalar()

    return {
        "total_alunos_ativos": total_alunos_ativos,
        "mensalidades_pendentes": mensalidades_pendentes,
        "mensalidades_vencidas": mensalidades_vencidas,
        "mensalidades_pagas": mensalidades_pagas,
        "valor_recebido": float(valor_recebido or 0),
        "valor_vencido": float(valor_vencido or 0)
    }