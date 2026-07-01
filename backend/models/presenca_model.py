from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from database import Base


class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=True)

    data_presenca = Column(Date, nullable=False)
    horario = Column(String(20), nullable=True)
    observacao = Column(Text, nullable=True)