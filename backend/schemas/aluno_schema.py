from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer
from typing import Literal


def converter_data_brasileira(valor):
    if valor is None or isinstance(valor, date):
        return valor

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("A data deve estar no formato dia/mês/ano. Exemplo: 28/06/2026")


class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    data_nascimento: date | None = None
    telefone: str | None = None
    endereco: str | None = None
    faixa_atual: Literal[
    "branca",
    "cinza",
    "amarela",
    "laranja",
    "verde",
    "azul",
    "roxa",
    "marrom",
    "preta"
] = "branca"
    graus_atual: int = Field(default=0, ge=0, le=4)
    data_matricula: date | None = None
    observacoes: str | None = None

    @field_validator("data_nascimento", "data_matricula", mode="before")
    @classmethod
    def validar_datas(cls, valor):
        return converter_data_brasileira(valor)

class AlunoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    data_nascimento: date | None = None
    telefone: str | None = None
    endereco: str | None = None
    faixa_atual: Literal[
    "branca",
    "cinza",
    "amarela",
    "laranja",
    "verde",
    "azul",
    "roxa",
    "marrom",
    "preta"
] | None = None
    graus_atual: int | None = Field(default=None, ge=0, le=4)
    ativo: bool | None = None
    data_matricula: date | None = None
    observacoes: str | None = None

    @field_validator("data_nascimento", "data_matricula", mode="before")
    @classmethod
    def validar_datas(cls, valor):
        return converter_data_brasileira(valor)


class AlunoResponse(BaseModel):
    id: int
    nome: str
    data_nascimento: date | None
    telefone: str | None
    endereco: str | None
    faixa_atual: str
    graus_atual: int
    ativo: bool
    data_matricula: date | None
    observacoes: str | None

    @field_serializer("data_nascimento", "data_matricula")
    def formatar_datas(self, valor):
        if valor is None:
            return None
        return valor.strftime("%d/%m/%Y")

    model_config = ConfigDict(from_attributes=True)