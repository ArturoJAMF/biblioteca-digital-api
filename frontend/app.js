const API_URL = "http://localhost:8000";

// =============================
// REGISTRAR LIBRO
// =============================
async function registrarLibro() {

    const data = {
        nombre: document.getElementById("nombre").value,
        autor: document.getElementById("autor").value,
        año: parseInt(document.getElementById("anio").value),
        paginas: parseInt(document.getElementById("paginas").value)
    };

    const response = await fetch(`${API_URL}/libros`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(JSON.stringify(result));
}


// =============================
// LISTAR LIBROS
// =============================
async function listarLibros() {

    const response = await fetch(`${API_URL}/libros`);
    const libros = await response.json();

    const lista = document.getElementById("listaLibros");
    lista.innerHTML = "";

    libros.forEach(libro => {
        const li = document.createElement("li");
        li.textContent = `ID: ${libro.id} | ${libro.nombre} | Estado: ${libro.estado}`;
        lista.appendChild(li);
    });
}


// =============================
// BUSCAR LIBRO
// =============================
async function buscarLibro() {

    const nombre = document.getElementById("buscarNombre").value;

    const response = await fetch(`${API_URL}/libros/buscar/${nombre}`);
    const libros = await response.json();

    alert(JSON.stringify(libros));
}


// =============================
// REGISTRAR PRÉSTAMO
// =============================
async function registrarPrestamo() {

    const data = {
        libro_id: parseInt(document.getElementById("libroId").value),
        usuario: {
            nombre: document.getElementById("usuarioNombre").value,
            correo: document.getElementById("usuarioCorreo").value
        }
    };

    const response = await fetch(`${API_URL}/prestamos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(JSON.stringify(result));
}


// =============================
// DEVOLVER LIBRO
// =============================
async function devolverLibro() {

    const id = document.getElementById("prestamoId").value;

    const response = await fetch(`${API_URL}/prestamos/devolver/${id}`, {
        method: "PUT"
    });

    const result = await response.json();
    alert(JSON.stringify(result));
}