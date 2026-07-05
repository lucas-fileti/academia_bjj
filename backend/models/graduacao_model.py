from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from database import Base


class Graduacao(Base):
    __tablename__ = "graduacoes"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)

    tipo = Column(String(20), nullable=False)
    faixa = Column(String(30), nullable=False)
    graus = Column(Integer, nullable=False, default=0)

    data_graduacao = Column(Date, nullable=False)
    observacao = Column(Text, nullable=True)