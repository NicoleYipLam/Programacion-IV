import os
import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_tarea_10")
API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5001")

@app.route('/')
def index():
    try:
        response = requests.get(f"{API_URL}/books", timeout=5)
        if response.status_code == 200:
            libros = response.json()
        else:
            libros = []
            flash("Error al obtener la lista de libros desde la API.", "error")
    except requests.exceptions.RequestException:
        libros = []
        flash("No se pudo conectar con el servidor de la API.", "error")
        
    return render_template('index.html', libros=libros)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    anio = request.form.get("anio", 2026)
    
    try:
        res = requests.post(
            f"{API_URL}/books",
            json={"titulo": titulo, "autor": autor, "anio": int(anio)},
            timeout=5
        )
        if res.status_code == 201:
            flash("Libro agregado correctamente.", "exito")
        else:
            flash("Error al agregar el libro. Verifica los datos.", "error")
    except requests.exceptions.RequestException:
        flash("Error de red al intentar guardar el libro.", "error")
        
    return redirect(url_for('index'))

@app.route('/editar/<int:libro_id>', methods=['POST'])
def editar(libro_id):
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    anio = request.form.get("anio")
    
    datos_actualizados = {}
    if titulo: datos_actualizados["titulo"] = titulo
    if autor: datos_actualizados["autor"] = autor
    if anio: datos_actualizados["anio"] = int(anio)

    try:
        res = requests.put(f"{API_URL}/books/{libro_id}", json=datos_actualizados, timeout=5)
        if res.status_code == 200:
            flash("Libro actualizado con exito.", "exito")
        else:
            flash("No se pudo actualizar el libro.", "error")
    except requests.exceptions.RequestException:
        flash("Error de conexion al actualizar.", "error")
        
    return redirect(url_for('index'))

@app.route('/eliminar/<int:libro_id>', methods=['POST'])
def eliminar(libro_id):
    try:
        res = requests.delete(f"{API_URL}/books/{libro_id}", timeout=5)
        if res.status_code == 200:
            flash("Libro eliminado correctamente.", "exito")
        else:
            flash("No se pudo eliminar el libro.", "error")
    except requests.exceptions.RequestException:
        flash("Error de conexion al eliminar.", "error")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)