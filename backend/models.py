from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from datetime import datetime


# MODELO LIBRO
class Libro(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre del libro entre 2 y 100 caracteres"
    )
    autor: str
    año: int
    paginas: int = Field(gt=1, description="Número de páginas mayor a 1")
    estado: Literal["disponible", "prestado"] = "disponible"

    @field_validator("año")
    @classmethod
    def validar_año(cls, value):
        año_actual = datetime.now().year
        if value <= 1450 or value > año_actual:
            raise ValueError("El año debe ser mayor a 1450 y menor o igual al año actual")
        return value


# MODELO USUARIO

class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


# MODELO PRESTAMO

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario