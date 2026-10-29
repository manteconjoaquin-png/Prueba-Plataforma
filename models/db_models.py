from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from config.database import Base


class Coleccion(Base):
    __tablename__ = "coleccion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    editorial = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)

    lanzamientos = relationship("Lanzamiento", back_populates="coleccion")
    suscripciones = relationship("Suscripcion", back_populates="coleccion")


class Lanzamiento(Base):
    __tablename__ = "lanzamiento"

    id = Column(Integer, primary_key=True, index=True)
    coleccion_id = Column(Integer, ForeignKey("coleccion.id"), nullable=False)
    entrega_numero = Column(Integer, nullable=False)
    titulo_entrega = Column(String, nullable=False)
    fecha_lanzamiento = Column(Date, nullable=False)

    coleccion = relationship("Coleccion", back_populates="lanzamientos")


class Suscripcion(Base):
    __tablename__ = "suscripcion"

    id = Column(Integer, primary_key=True, index=True)
    coleccion_id = Column(Integer, ForeignKey("coleccion.id"), nullable=False)
    user_email = Column(String, nullable=False)
    fecha_alta = Column(DateTime, default=datetime.utcnow, nullable=False)

    coleccion = relationship("Coleccion", back_populates="suscripciones")