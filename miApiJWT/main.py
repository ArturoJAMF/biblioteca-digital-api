from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from models import Libro, Prestamo
from database import libros, prestamos
from auth import authenticate_user, create_access_token, get_current_user

# CREAR APP

app = FastAPI(title="API Biblioteca Digital - JWT")

@app.get("/")
def home():
    return {"mensaje": "API Biblioteca Digital funcionando correctamente"}

# CONFIGURAR CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOGIN → GENERAR TOKEN JWT

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = create_access_token(
        data={"sub": form_data.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ENDPOINTS LIBROS

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El libro ya existe"
            )

    nuevo_libro = libro.model_dump()
    nuevo_libro["id"] = len(libros) + 1
    nuevo_libro["estado"] = "disponible"

    libros.append(nuevo_libro)

    return {
        "mensaje": "Libro registrado correctamente",
        "libro": nuevo_libro
    }


@app.get("/libros", status_code=status.HTTP_200_OK)
def listar_libros():
    return libros


@app.get("/libros/buscar/{nombre}", status_code=status.HTTP_200_OK)
def buscar_libro(nombre: str):

    resultados = [
        libro for libro in libros
        if nombre.lower() in libro["nombre"].lower()
    ]

    return resultados


# ENDPOINTS PRÉSTAMOS

@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):

    libro = next(
        (l for l in libros if l["id"] == prestamo.libro_id),
        None
    )

    if not libro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Libro no encontrado"
        )

    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya está prestado"
        )

    libro["estado"] = "prestado"

    nuevo_prestamo = prestamo.model_dump()
    nuevo_prestamo["id"] = len(prestamos) + 1

    prestamos.append(nuevo_prestamo)

    return {
        "mensaje": "Préstamo registrado correctamente",
        "prestamo": nuevo_prestamo
    }


# ENDPOINT PROTEGIDO → DEVOLVER

@app.put("/prestamos/devolver/{prestamo_id}",
         status_code=status.HTTP_200_OK)
def devolver_libro(
    prestamo_id: int,
    usuario: str = Depends(get_current_user)
):

    prestamo = next(
        (p for p in prestamos if p["id"] == prestamo_id),
        None
    )

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El préstamo no existe"
        )

    libro = next(
        (l for l in libros if l["id"] == prestamo["libro_id"]),
        None
    )

    if libro:
        libro["estado"] = "disponible"

    return {
        "mensaje": f"Libro devuelto correctamente por {usuario}"
    }


# ENDPOINT PROTEGIDO → ELIMINAR

@app.delete("/prestamos/{prestamo_id}",
            status_code=status.HTTP_200_OK)
def eliminar_prestamo(
    prestamo_id: int,
    usuario: str = Depends(get_current_user)
):

    prestamo = next(
        (p for p in prestamos if p["id"] == prestamo_id),
        None
    )

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El préstamo no existe"
        )

    prestamos.remove(prestamo)

    return {
        "mensaje": f"Préstamo eliminado correctamente por {usuario}"
    }