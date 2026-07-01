from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    observacao = Column(Text, nullable=True)