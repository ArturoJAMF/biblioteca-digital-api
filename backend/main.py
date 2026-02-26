from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import Libro, Prestamo

# =============================
# CREAR APP
# =============================
app = FastAPI(title="API Biblioteca Digital")

# =============================
# CONFIGURAR CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# BASE DE DATOS EN MEMORIA
# =============================
libros = []
prestamos = []

# =====================================================
# ================== ENDPOINTS LIBROS =================
# =====================================================

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    # Verificar si ya existe libro con mismo nombre
    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El libro ya existe"
            )

    nuevo_libro = libro.model_dump()
    nuevo_libro["id"] = len(libros) + 1

    libros.append(nuevo_libro)

    return nuevo_libro


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


# =====================================================
# ================= ENDPOINTS PRESTAMOS ===============
# =====================================================

@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):

    # Buscar libro por ID
    libro = next((l for l in libros if l["id"] == prestamo.libro_id), None)

    if not libro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Libro no encontrado"
        )

    # Verificar si ya está prestado
    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya está prestado"
        )

    # Cambiar estado del libro
    libro["estado"] = "prestado"

    nuevo_prestamo = prestamo.model_dump()
    nuevo_prestamo["id"] = len(prestamos) + 1

    prestamos.append(nuevo_prestamo)

    return nuevo_prestamo


@app.put("/prestamos/devolver/{prestamo_id}", status_code=status.HTTP_200_OK)
def devolver_libro(prestamo_id: int):

    prestamo = next((p for p in prestamos if p["id"] == prestamo_id), None)

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo no existe"
        )

    libro = next((l for l in libros if l["id"] == prestamo["libro_id"]), None)

    if libro:
        libro["estado"] = "disponible"

    return {"mensaje": "Libro devuelto correctamente"}


@app.delete("/prestamos/{prestamo_id}", status_code=status.HTTP_200_OK)
def eliminar_prestamo(prestamo_id: int):

    prestamo = next((p for p in prestamos if p["id"] == prestamo_id), None)

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo no existe"
        )

    prestamos.remove(prestamo)

    return {"mensaje": "Préstamo eliminado correctamente"}