from pydantic import BaseModel, Field, ConfigDict


class ProfessorCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str | None = None
    observacao: str | None = None


class ProfessorUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    telefone: str | None = None
    ativo: bool | None = None
    observacao: str | None = None


class ProfessorResponse(BaseModel):
    id: int
    nome: str
    telefone: str | None
    ativo: bool
    observacao: str | None

    model_config = ConfigDict(from_attributes=True)