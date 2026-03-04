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

    autor: str = Field(
        min_length=2,
        max_length=100
    )

    anio: int
    paginas: int

    @field_validator("anio")
    @classmethod
    def validar_anio(cls, value):
        current_year = datetime.now().year

        if value <= 1450 or value > current_year:
            raise ValueError(
                f"El año debe ser mayor a 1450 y menor o igual a {current_year}"
            )
        return value

    @field_validator("paginas")
    @classmethod
    def validar_paginas(cls, value):
        if value <= 1:
            raise ValueError("Las páginas deben ser un número entero mayor a 1")
        return value



# MODELO USUARIO
class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr



# MODELO PRESTAMO
class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario


# ESTADO DEL LIBRO
EstadoLibro = Literal["disponible", "prestado"]