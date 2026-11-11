from flask import Flask, render_template, request, redirect, url_for, flash
import redis
import uuid
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Conexión con KeyDB
keydb = redis.Redis(
    host=Config.KEYDB_HOST,
    port=Config.KEYDB_PORT,
    db=Config.KEYDB_DB,
    decode_responses=True
)

# Verificar conexión
def verificar_keydb():
    return keydb.ping()

# Obtener todos los libros
def obtener_libros():
    libros = []
    ids = keydb.smembers("libros")

    for libro_id in ids:
        libro = keydb.hgetall(f"libro:{libro_id}")

        if libro:
            libro["id"] = libro_id
            libros.append(libro)

    return sorted(libros, key=lambda x: x["titulo"].lower())


# Página principal y búsqueda
@app.route("/")
def inicio():
    busqueda = request.args.get("buscar", "").strip().lower()
    libros = obtener_libros()

    if busqueda:
        libros = [
            libro for libro in libros
            if busqueda in libro["titulo"].lower()
            or busqueda in libro["autor"].lower()
            or busqueda in libro["genero"].lower()
        ]

    return render_template("index.html", libros=libros)


# Agregar un libro
@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form.get("titulo", "").strip()
    autor = request.form.get("autor", "").strip()
    genero = request.form.get("genero", "").strip()
    estado = request.form.get("estado", "").strip()

    if not all([titulo, autor, genero, estado]):
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("inicio"))

    if estado not in ["Pendiente", "Leyendo", "Leído"]:
        flash("Estado de lectura no válido.", "danger")
        return redirect(url_for("inicio"))

    for libro in obtener_libros():
        if (libro["titulo"].lower() == titulo.lower()
                and libro["autor"].lower() == autor.lower()):
            flash("Este libro ya está registrado.", "warning")
            return redirect(url_for("inicio"))

    libro_id = str(uuid.uuid4())

    keydb.hset(
        f"libro:{libro_id}",
        mapping={
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }
    )

    keydb.sadd("libros", libro_id)

    flash("¡Libro agregado correctamente!", "success")
    return redirect(url_for("inicio"))


# Editar un libro
@app.route("/editar/<libro_id>", methods=["GET", "POST"])
def editar(libro_id):
    clave = f"libro:{libro_id}"

    if not keydb.exists(clave):
        flash("El libro no existe.", "danger")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        estado = request.form.get("estado", "").strip()

        if not all([titulo, autor, genero, estado]):
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for("editar", libro_id=libro_id))

        if estado not in ["Pendiente", "Leyendo", "Leído"]:
            flash("Estado de lectura no válido.", "danger")
            return redirect(url_for("editar", libro_id=libro_id))

        for libro in obtener_libros():
            if (libro["id"] != libro_id
                    and libro["titulo"].lower() == titulo.lower()
                    and libro["autor"].lower() == autor.lower()):
                flash("Ya existe otro libro con ese título y autor.", "warning")
                return redirect(url_for("editar", libro_id=libro_id))

        keydb.hset(
            clave,
            mapping={
                "titulo": titulo,
                "autor": autor,
                "genero": genero,
                "estado": estado
            }
        )

        flash("¡Libro actualizado correctamente!", "success")
        return redirect(url_for("inicio"))

    libro = keydb.hgetall(clave)
    libro["id"] = libro_id

    return render_template("editar.html", libro=libro)


# Eliminar un libro
@app.route("/eliminar/<libro_id>", methods=["POST"])
def eliminar(libro_id):
    clave = f"libro:{libro_id}"

    if keydb.exists(clave):
        keydb.delete(clave)
        keydb.srem("libros", libro_id)
        flash("Libro eliminado correctamente.", "success")
    else:
        flash("El libro no existe.", "danger")

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
