from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer


def converter_data_brasileira(valor):
    if valor is None or isinstance(valor, date):
        return valor

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("A data deve estar no formato dia/mês/ano. Exemplo: 01/07/2026")


class PresencaCreate(BaseModel):
    aluno_id: int
    professor_id: int | None = None
    data_presenca: date
    horario: str | None = None
    observacao: str | None = None

    @field_validator("data_presenca", mode="before")
    @classmethod
    def validar_data_presenca(cls, valor):
        return converter_data_brasileira(valor)


class PresencaResponse(BaseModel):
    id: int
    aluno_id: int
    professor_id: int | None
    data_presenca: date
    horario: str | None
    observacao: str | None

    @field_serializer("data_presenca")
    def formatar_data_presenca(self, valor):
        if valor is None:
            return None
        return valor.strftime("%d/%m/%Y")

    model_config = ConfigDict(from_attributes=True)