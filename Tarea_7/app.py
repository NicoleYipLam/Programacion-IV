
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Clave para los mensajes flash
app.secret_key = "mi_biblioteca_2026"

# Lista donde guardaremos nuestros libros
libros = []

# Contador para identificar cada libro
contador_id = 1


# Página principal
@app.route("/")
def index():
    return render_template("index.html", libros=libros)


# Agregar un nuevo libro
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    global contador_id

    if request.method == "POST":

        titulo = request.form["titulo"]
        autor = request.form["autor"]
        anio = request.form["anio"]

        nuevo_libro = {
            "id": contador_id,
            "titulo": titulo,
            "autor": autor,
            "anio": anio
        }

        libros.append(nuevo_libro)
        contador_id += 1

        flash("Libro agregado correctamente", "success")

        return redirect(url_for("index"))

    return render_template("agregar.html")


# Editar un libro existente
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    libro = next(
        (l for l in libros if l["id"] == id),
        None
    )

    if libro is None:
        flash("Libro no encontrado", "error")
        return redirect(url_for("index"))

    if request.method == "POST":

        libro["titulo"] = request.form["titulo"]
        libro["autor"] = request.form["autor"]
        libro["anio"] = request.form["anio"]

        flash("Libro actualizado correctamente", "success")

        return redirect(url_for("index"))

    return render_template("editar.html", libro=libro)


# Eliminar un libro
@app.route("/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar(id):

    libro = next(
        (l for l in libros if l["id"] == id),
        None
    )

    if libro is None:
        flash("Libro no encontrado", "error")
        return redirect(url_for("index"))

    if request.method == "POST":

        libros.remove(libro)

        flash("Libro eliminado correctamente", "success")

        return redirect(url_for("index"))

    return render_template("eliminar.html", libro=libro)


# Buscar libros
@app.route("/buscar")
def buscar():

    termino = request.args.get("q", "").strip().lower()

    resultados = [
        libro for libro in libros
        if termino in libro["titulo"].lower()
        or termino in libro["autor"].lower()
    ]

    return render_template(
        "buscar.html",
        resultados=resultados,
        termino=termino
    )

# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)
