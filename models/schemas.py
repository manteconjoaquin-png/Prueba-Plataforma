import re
from datetime import date

from pydantic import BaseModel, field_validator


class ColeccionBase(BaseModel):
    nombre: str
    editorial: str
    descripcion: str


class ColeccionCreate(ColeccionBase):
    pass


class ColeccionResponse(ColeccionBase):
    id: int

    class Config:
        from_attributes = True


class LanzamientoBase(BaseModel):
    coleccion_id: int
    entrega_numero: int
    titulo_entrega: str
    fecha_lanzamiento: date


class LanzamientoCreate(LanzamientoBase):
    pass


class LanzamientoResponse(LanzamientoBase):
    id: int

    class Config:
        from_attributes = True


class SuscripcionCreate(BaseModel):
    coleccion_id: int
    user_email: str

    @field_validator("user_email")
    @classmethod
    def validate_user_email(cls, value: str) -> str:
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is None:
            raise ValueError("user_email debe tener un formato de correo válido")
        return value