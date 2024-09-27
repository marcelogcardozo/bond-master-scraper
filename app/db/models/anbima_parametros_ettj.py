from datetime import datetime as dt

from sqlalchemy import Column, Date, DateTime, Float, String

from app.db.base import Base


class ANBIMAParametrosETTJ(Base):
    __tablename__ = "PARAMETROS_CURVA_ETTJ"
    __table_args__ = {"schema": "anbima"}

    nome_taxa = Column(String(20), primary_key=True, nullable=False)
    data = Column(Date, primary_key=True, nullable=False)
    beta1 = Column(Float, nullable=False)
    beta2 = Column(Float, nullable=False)
    beta3 = Column(Float, nullable=False)
    beta4 = Column(Float, nullable=False)
    lambda1 = Column(Float, nullable=False)
    lambda2 = Column(Float, nullable=False)

    updated = Column(DateTime, default=dt.now(), nullable=False)

    def __repr__(self):
        return f"<ANBIMAParametrosETTJ(nome_taxa={self.nome_taxa}, data={self.data}, beta1={self.beta1}, beta2={self.beta2}, beta3={self.beta3}, beta4={self.beta4}, lambda1={self.lambda1}, lambda2={self.lambda2})>"
