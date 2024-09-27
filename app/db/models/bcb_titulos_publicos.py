from datetime import datetime as dt

from sqlalchemy import Boolean, Column, Date, DateTime, Float, String

from app.db.base import Base


class BCBTitulosPublicos(Base):
    __tablename__ = "TITULOS_PUBLICOS"
    __table_args__ = {"schema": "bcb"}

    codigo_isin = Column(String(12))
    sigla_titulo = Column(String(10), primary_key=True)
    codigo_titulo = Column(String(10), primary_key=True)
    data_vencimento = Column(Date, primary_key=True)
    data_primeira_emissao = Column(Date)
    valor_nominal_data_base = Column(Float)
    valor_resgate = Column(Float)
    paga_cupom = Column(Boolean)
    frequencia_cupom = Column(String(10))
    taxa_cupom = Column(Float)

    updated = Column(DateTime, default=dt.now())

    def __repr__(self):
        return f"<BCBTitulosPublicos(sigla_titulo={self.sigla_titulo}, codigo_titulo={self.codigo_titulo}, data_vencimento={self.data_vencimento}, codigo_isin={self.codigo_isin})>"
