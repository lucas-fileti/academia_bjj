from sqlalchemy import Column,  Integer, String, Date, Text, Numeric, ForeignKey
from database import Base

class Mensalidade(Base):
    __tablename__ = "mensalidades"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"),nullable=False)

    valor = Column(Numeric(10,2),nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date,nullable=True)

    status = Column(String(20), nullable=False, default="pendente")
    forma_pagamento = Column(String(30), nullable=True)
    observacao = Column(Text,nullable=True)