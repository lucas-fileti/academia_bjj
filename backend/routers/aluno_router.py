from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.aluno_model import Aluno
from schemas.aluno_schema import AlunoCreate, AlunoResponse, AlunoUpdate

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


@router.post("/", response_model=AlunoResponse)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    novo_aluno = Aluno(**aluno.model_dump())

    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)

    return novo_aluno


@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(
    mostrar_inativos: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Aluno)

    if not mostrar_inativos:
        query = query.filter(Aluno.inativo == True)
    
    alunos = query.all()

    return alunos

@router.patch("/{aluno_id}", response_model=AlunoResponse)
def editar_aluno(
    aluno_id: int,
    alunos_dados: AlunoUpdate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(
            status_code=404, detail="Aluno não encontrado"
            )
    
    dados_atualizados = alunos_dados.model_dump(exclude_unset=True)
    
    for campo, valor in dados_atualizados.items():
        setattr(aluno, campo, valor)

    db.commit()
    db.refresh(aluno)

    return aluno

@router.delete("/{aluno_id}", response_model=AlunoResponse)
def inativar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(
            status_code=404, detail="Aluno não encontrado"
            )
    
    aluno.ativo = False

    db.commit()
    db.refresh(aluno)

    return aluno