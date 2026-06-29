from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.aluno_model import Aluno
from models.mensalidade_model import Mensalidade
from schemas.mensalidade_schema import MensalidadeCreate, MensalidadeResponse


router = APIRouter(
    prefix="/mensalidades",
    tags=["Mensalidades"]
)


@router.post("/", response_model=MensalidadeResponse)
def criar_mensalidade(
    mensalidade: MensalidadeCreate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == mensalidade.aluno_id).first()

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    if aluno.ativo is False:
        raise HTTPException(
            status_code=400,
            detail="Não é possível cadastrar mensalidade para aluno inativo"
        )

    nova_mensalidade = Mensalidade(**mensalidade.model_dump())

    db.add(nova_mensalidade)
    db.commit()
    db.refresh(nova_mensalidade)

    return nova_mensalidade


@router.get("/", response_model=list[MensalidadeResponse])
def listar_mensalidades(db: Session = Depends(get_db)):
    mensalidades = db.query(Mensalidade).all()
    return mensalidades