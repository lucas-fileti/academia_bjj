from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer
from typing import Literal


def converter_data_brasileira(valor):
    if valor is None or isinstance(valor, date):
        return valor

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("A data deve estar no formato dia/mês/ano. Exemplo: 10/07/2026")


class MensalidadeCreate(BaseModel):
    aluno_id: int
    valor: float = Field(..., gt=0)
    data_vencimento: date
    data_pagamento: date | None = None
    status: Literal["pendente", "paga", "vencida", "cancelada"] = "pendente"
    forma_pagamento: str | None = None
    observacao: str | None = None

    @field_validator("data_vencimento", "data_pagamento", mode="before")
    @classmethod
    def validar_datas(cls, valor):
        return converter_data_brasileira(valor)    

class MensalidadePagar(BaseModel):
    data_pagamento: date
    forma_pagamento: Literal["pix", "cartao", "dinheiro"]

    @field_validator("data_pagamento", mode="before")
    @classmethod
    def validar_data_pagamento(cls, valor):
        return converter_data_brasileira(valor)


class MensalidadeUpdate(BaseModel):
    valor: float | None = Field(default=None, gt=0)
    data_vencimento: date | None = None
    data_pagamento: date | None = None
    status: Literal["pendente", "paga", "vencida", "cancelada"] | None = None
    forma_pagamento: str | None = None
    observacao: str | None = None

    @field_validator("data_vencimento", "data_pagamento", mode="before")
    @classmethod
    def validar_datas(cls, valor):
        return converter_data_brasileira(valor)

class MensalidadeResponse(BaseModel):
    id: int
    aluno_id: int
    valor: float
    data_vencimento: date
    data_pagamento: date | None
    status: str
    forma_pagamento: str | None
    observacao: str | None

    @field_serializer("data_vencimento", "data_pagamento")
    def formatar_datas(self, valor):
        if valor is None:
            return None
        return valor.strftime("%d/%m/%Y")

    model_config = ConfigDict(from_attributes=True)