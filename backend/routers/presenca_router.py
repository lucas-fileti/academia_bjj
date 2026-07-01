from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime

from database import get_db
from models.aluno_model import Aluno
from models.professor_model import Professor
from models.presenca_model import Presenca
from schemas.presenca_schema import PresencaCreate, PresencaResponse


router = APIRouter(
    prefix="/presencas",
    tags=["Presenças"]
)

def converter_data_brasileira(valor: str | None):
    if valor is None:
        return None

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="A data deve estar no formato dia/mês/ano. Exemplo: 01/07/2026"
        )

@router.post("/", response_model=PresencaResponse)
def registrar_presenca(
    presenca: PresencaCreate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == presenca.aluno_id).first()

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    if aluno.ativo is False:
        raise HTTPException(
            status_code=400,
            detail="Não é possível registrar presença para aluno inativo"
        )

    if presenca.professor_id is not None:
        professor = db.query(Professor).filter(
            Professor.id == presenca.professor_id
        ).first()

        if professor is None:
            raise HTTPException(
                status_code=404,
                detail="Professor não encontrado"
            )

        if professor.ativo is False:
            raise HTTPException(
                status_code=400,
                detail="Não é possível registrar presença com professor inativo"
            )

    nova_presenca = Presenca(**presenca.model_dump())

    db.add(nova_presenca)
    db.commit()
    db.refresh(nova_presenca)

    return nova_presenca

@router.get("/", response_model=list[PresencaResponse])
def listar_presencas(
    aluno_id: int | None = None,
    professor_id: int | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Presenca)

    if aluno_id is not None:
        query = query.filter(Presenca.aluno_id == aluno_id)

    if professor_id is not None:
        query = query.filter(Presenca.professor_id == professor_id)

    data_inicio_convertida = converter_data_brasileira(data_inicio)
    data_fim_convertida = converter_data_brasileira(data_fim)

    if data_inicio_convertida is not None:
        query = query.filter(Presenca.data_presenca >= data_inicio_convertida)

    if data_fim_convertida is not None:
        query = query.filter(Presenca.data_presenca <= data_fim_convertida)

    presencas = query.all()

    return presencas