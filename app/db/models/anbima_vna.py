from datetime import datetime as dt

from sqlalchemy import Column, Date, DateTime, Float, String

from app.db.base import Base


class ANBIMAVNA(Base):
    __tablename__ = "VNA"
    __table_args__ = {"schema": "anbima"}

    titulo = Column(String(10), primary_key=True, nullable=False)
    codigo_selic = Column(String(10), primary_key=True, nullable=False)
    data = Column(Date, primary_key=True, nullable=False)
    vna = Column(Float, nullable=False)

    updated = Column(DateTime, default=dt.now(), nullable=False)

    def __repr__(self):
        return f"<ANBIMAVNA(titulo={self.titulo}, codigo_selic={self.codigo_selic}, data={self.data}, vna={self.vna})>"
