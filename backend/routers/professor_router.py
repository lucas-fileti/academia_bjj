from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.professor_model import Professor
from schemas.professor_schema import ProfessorCreate, ProfessorUpdate, ProfessorResponse


router = APIRouter(
    prefix="/professores",
    tags=["Professores"]
)


@router.post("/", response_model=ProfessorResponse)
def criar_professor(
    professor: ProfessorCreate,
    db: Session = Depends(get_db)
):
    novo_professor = Professor(**professor.model_dump())

    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return novo_professor


@router.get("/", response_model=list[ProfessorResponse])
def listar_professores(
    mostrar_inativos: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Professor)

    if not mostrar_inativos:
        query = query.filter(Professor.ativo == True)

    professores = query.all()

    return professores


@router.patch("/{professor_id}", response_model=ProfessorResponse)
def editar_professor(
    professor_id: int,
    professor_dados: ProfessorUpdate,
    db: Session = Depends(get_db)
):
    professor = db.query(Professor).filter(Professor.id == professor_id).first()

    if professor is None:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado"
        )

    dados_atualizados = professor_dados.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(professor, campo, valor)

    db.commit()
    db.refresh(professor)

    return professor


@router.delete("/{professor_id}", response_model=ProfessorResponse)
def inativar_professor(
    professor_id: int,
    db: Session = Depends(get_db)
):
    professor = db.query(Professor).filter(Professor.id == professor_id).first()

    if professor is None:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado"
        )

    professor.ativo = False

    db.commit()
    db.refresh(professor)

    return professor