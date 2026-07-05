from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer


def converter_data_brasileira(valor):
    if valor is None or isinstance(valor, date):
        return valor

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("A data deve estar no formato dia/mês/ano. Exemplo: 01/07/2026")


class GraduacaoCreate(BaseModel):
    aluno_id: int

    tipo: Literal["faixa", "grau"]

    faixa: Literal[
        "branca",
        "cinza",
        "amarela",
        "laranja",
        "verde",
        "azul",
        "roxa",
        "marrom",
        "preta"
    ]

    graus: int = Field(..., ge=0, le=4)
    data_graduacao: date
    observacao: str | None = None

    @field_validator("data_graduacao", mode="before")
    @classmethod
    def validar_data_graduacao(cls, valor):
        return converter_data_brasileira(valor)


class GraduacaoResponse(BaseModel):
    id: int
    aluno_id: int
    tipo: str
    faixa: str
    graus: int
    data_graduacao: date
    observacao: str | None

    @field_serializer("data_graduacao")
    def formatar_data_graduacao(self, valor):
        if valor is None:
            return None
        return valor.strftime("%d/%m/%Y")

    model_config = ConfigDict(from_attributes=True)