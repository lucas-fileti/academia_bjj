from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Literal

from database import get_db
from models.aluno_model import Aluno
from models.graduacao_model import Graduacao
from schemas.graduacao_schema import GraduacaoCreate, GraduacaoResponse


router = APIRouter(
    prefix="/graduacoes",
    tags=["Graduações"]
)


@router.post("/", response_model=GraduacaoResponse)
def registrar_graduacao(
    graduacao: GraduacaoCreate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == graduacao.aluno_id).first()

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    if aluno.ativo is False:
        raise HTTPException(
            status_code=400,
            detail="Não é possível registrar graduação para aluno inativo"
        )

    nova_graduacao = Graduacao(**graduacao.model_dump())

    aluno.faixa_atual = graduacao.faixa
    aluno.graus_atual = graduacao.graus

    db.add(nova_graduacao)
    db.commit()
    db.refresh(nova_graduacao)

    return nova_graduacao

@router.get("/ultimas", response_model=list[GraduacaoResponse])
def listar_ultimas_graduacoes(
    limite: int = 5,
    db: Session = Depends(get_db)
):
    graduacoes = db.query(Graduacao).order_by(
        Graduacao.data_graduacao.desc()
    ).limit(limite).all()

    return graduacoes

@router.get("/", response_model=list[GraduacaoResponse])
def listar_graduacoes(
    aluno_id: int | None = None,
    tipo: Literal["faixa", "grau"] | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Graduacao)

    if aluno_id is not None:
        query = query.filter(Graduacao.aluno_id == aluno_id)

    if tipo is not None:
        query = query.filter(Graduacao.tipo == tipo)

    graduacoes = query.all()

    return graduacoes

@router.get("/aluno/{aluno_id}/ultima", response_model=GraduacaoResponse)
def buscar_ultima_graduacao_do_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    graduacao = db.query(Graduacao).filter(
        Graduacao.aluno_id == aluno_id
    ).order_by(
        Graduacao.data_graduacao.desc()
    ).first()

    if graduacao is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma graduação encontrada para este aluno"
        )

    return graduacao