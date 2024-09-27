from datetime import datetime as dt

from sqlalchemy import Column, Date, Float

from app.db.base import Base


class BCBSelic(Base):
    __tablename__ = "SELIC_HISTORICO"
    __table_args__ = {"schema": "bcb"}

    data = Column(Date, primary_key=True, nullable=False)
    fator_diario = Column(Float, nullable=False)
    taxa_anual = Column(Float, nullable=False)
    updated = Column(Date, default=dt.now(), nullable=False)

    def __repr__(self):
        return f"<BCBSelic(data_cotacao={self.data_cotacao}, fator_diario={self.fator_diario}, taxa_anual={self.taxa_anual})>"
