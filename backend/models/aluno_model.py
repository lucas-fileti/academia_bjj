from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True)

    faixa_atual = Column(String(30), nullable=False, default="branca")
    graus_atual = Column(Integer, nullable=False, default=0)

    ativo = Column(Boolean, nullable=False, default=True)
    data_matricula = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)