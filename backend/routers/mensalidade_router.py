from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.aluno_model import Aluno
from models.mensalidade_model import Mensalidade
from schemas.mensalidade_schema import MensalidadeCreate, MensalidadeUpdate, MensalidadeResponse, MensalidadePagar


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
def listar_mensalidades(
    aluno_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    
    query = db.query(Mensalidade)

    if aluno_id is not None:
        query = query.filter(Mensalidade.aluno_id == aluno_id)

    if status is not None:
        query = query.filter(Mensalidade.status == status)
    
    mensalidades = query.all()

    return mensalidades 
    

@router.patch("/{mensalidade_id}", response_model=MensalidadeResponse)
def editar_mensalidade(
    mensalidade_id: int,
    mensalidade_dados: MensalidadeUpdate,
    db: Session = Depends(get_db)
):
    mensalidade = db.query(Mensalidade).filter(Mensalidade.id == mensalidade_id).first()

    if mensalidade is None:
        raise HTTPException(
            status_code=404,
            detail="Mensalidade não encontrada"
        )

    dados_atualizados = mensalidade_dados.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(mensalidade, campo, valor)

    db.commit()
    db.refresh(mensalidade)

    return mensalidade


@router.patch("/{mensalidade_id}/pagar", response_model=MensalidadeResponse)
def pagar_mensalidade(
    mensalidade_id: int,
    dados_pagamento: MensalidadePagar,
    db: Session = Depends(get_db)
):
    mensalidade = db.query(Mensalidade).filter(Mensalidade.id == mensalidade_id).first()

    if mensalidade is None:
        raise HTTPException(
            status_code=404,
            detail="Mensalidade não encontrada"
        )

    mensalidade.status = "paga"
    mensalidade.data_pagamento = dados_pagamento.data_pagamento
    mensalidade.forma_pagamento = dados_pagamento.forma_pagamento

    db.commit()
    db.refresh(mensalidade)

    return mensalidade


@router.patch("/{mensalidade_id}/cancelar", response_model=MensalidadeResponse)
def cancelar_mensalidade(
    mensalidade_id: int,
    db: Session = Depends(get_db)
):
    mensalidade = db.query(Mensalidade).filter(Mensalidade.id == mensalidade_id).first()

    if mensalidade is None:
        raise HTTPException(
            status_code=404,
            detail="Mensalidade não encontrada"
        )

    mensalidade.status = "cancelada"

    db.commit()
    db.refresh(mensalidade)

    return mensalidade