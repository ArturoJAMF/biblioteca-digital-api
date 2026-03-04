from typing import List, Dict

# LIBROS (SIMULACIÓN DE BASE DE DATOS)


libros : List[Dict] = [
    {
        "id": 1,
        "nombre": "Clean Code",
        "autor": "Robert C. Martin",
        "anio": 2008,
        "paginas": 464,
        "estado": "disponible"
    },
    {
        "id": 2,
        "nombre": "Python Crash Course",
        "autor": "Eric Matthes",
        "anio": 2019,
        "paginas": 544,
        "estado": "disponible"
    }
]

# PRÉSTAMOS


prestamos : List[Dict] = []

# CONTADORES AUTOMÁTICOS (IDs)

book_id_counter = len(libros) + 1
loan_id_counter = 1


# FUNCIONES AUXILIARES

def get_next_book_id():
    global book_id_counter
    current_id = book_id_counter
    book_id_counter += 1
    return current_id


def get_next_loan_id():
    global loan_id_counter
    current_id = loan_id_counter
    loan_id_counter += 1
    return current_id


def find_book_by_id(book_id: int):
    for book in libros:
        if book["id"] == book_id:
            return book
    return None


def find_book_by_name(name: str):
    results = []
    for book in libros:
        if name.lower() in book["nombre"].lower():
            results.append(book)
    return results


def find_loan_by_id(loan_id: int):
    for loan in prestamos:
        if loan["id"] == loan_id:
            return loan
    return None