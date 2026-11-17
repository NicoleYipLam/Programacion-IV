from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada en memoria para los libros
libros = [
    {"id": 1, "titulo": "Cien anos de soledad", "autor": "Gabriel Garcia Marquez", "anio": 1967},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "anio": 1949}
]

# GET /books -> Obtener todos los libros
@app.route('/books', methods=['GET'])
def obtener_libros():
    return jsonify(libros), 200

# GET /books/<id> -> Obtener un libro especifico
@app.route('/books/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    libro = next((l for l in libros if l["id"] == libro_id), None)
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify(libro), 200

# POST /books -> Agregar un nuevo libro
@app.route('/books', methods=['POST'])
def agregar_libro():
    data = request.get_json()
    
    if not data or not "titulo" in data or not "autor" in data:
        return jsonify({"error": "Faltan datos obligatorios (titulo, autor)"}), 400
        
    nuevo_id = max([l["id"] for l in libros], default=0) + 1
    nuevo_libro = {
        "id": nuevo_id,
        "titulo": data["titulo"],
        "autor": data["autor"],
        "anio": data.get("anio", 2024)
    }
    libros.append(nuevo_libro)
    return jsonify(nuevo_libro), 201

# PUT /books/<id> -> Actualizar un libro
@app.route('/books/<int:libro_id>', methods=['PUT'])
def actualizar_libro(libro_id):
    libro = next((l for l in libros if l["id"] == libro_id), None)
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos invalidos"}), 400
        
    libro["titulo"] = data.get("titulo", libro["titulo"])
    libro["autor"] = data.get("autor", libro["autor"])
    libro["anio"] = data.get("anio", libro["anio"])
    
    return jsonify(libro), 200

# DELETE /books/<id> -> Eliminar un libro
@app.route('/books/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):
    global libros
    libro = next((l for l in libros if l["id"] == libro_id), None)
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404
        
    libros = [l for l in libros if l["id"] != libro_id]
    return jsonify({"mensaje": f"Libro {libro_id} eliminado con exito"}), 200

if __name__ == '__main__':
    # La API correra en el puerto 5001
    app.run(debug=True, port=5001)