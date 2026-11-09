from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson.objectid import ObjectId

# Configuración de la conexión a MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "biblioteca_db"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    collection = db["libros"]
    print("¡Conexión exitosa a MongoDB!")
except ConnectionFailure as e:
    print(f"Error crítico: No se pudo conectar a MongoDB. Detalle: {e}")
    client = None
    collection = None

def menu():
    if collection is None:
        print("La aplicación no puede iniciar debido a un error de conexión con la base de datos.")
        return

    while True:
        print("\n======================================")
        print("   BIBLIOTECA PERSONAL MONGODB (NoSQL)")
        print("======================================")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros (Título, Autor o Género)")
        print("6. Salir")
        
        opcion = input("\nElige una opción (1-6): ").strip()

        try:
            if opcion == "1":
                print("\n--- Agregar Nuevo Libro ---")
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                genero = input("Género: ").strip()
                estado = input("Estado de lectura (Pendiente / Leyendo / Leído): ").strip()

                if not titulo or not autor:
                    print("Error: El título y el autor son campos obligatorios.")
                    continue

                nuevo_libro = {
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "estado_de_lectura": estado
                }
                
                collection.insert_one(nuevo_libro)
                print("¡Libro agregado exitosamente como documento JSON!")

            elif opcion == "2":
                print("\n--- Actualizar Libro ---")
                libros = list(collection.find())
                if not libros:
                    print("No hay libros registrados para actualizar.")
                    continue

                for l in libros:
                    print(f"ID: {l['_id']} | Título: {l['titulo']} - Autor: {l['autor']}")
                
                libro_id_str = input("\nIngresa el ID del documento que deseas actualizar: ").strip()
                
                try:
                    obj_id = ObjectId(libro_id_str)
                except Exception:
                    print("Error: El ID ingresado no tiene un formato válido para MongoDB.")
                    continue

                libro_actual = collection.find_one({"_id": obj_id})
                if not libro_actual:
                    print("No se encontró ningún libro con ese ID.")
                    continue

                print(f"Editando a: {libro_actual['titulo']}. Deja en blanco si no quieres cambiar el dato.")
                nuevo_titulo = input(f"Nuevo título [{libro_actual.get('titulo', '')}]: ").strip()
                nuevo_autor = input(f"Nuevo autor [{libro_actual.get('autor', '')}]: ").strip()
                nuevo_genero = input(f"Nuevo género [{libro_actual.get('genero', '')}]: ").strip()
                nuevo_estado = input(f"Nuevo estado [{libro_actual.get('estado_de_lectura', '')}]: ").strip()

                updates = {}
                if nuevo_titulo: updates["titulo"] = nuevo_titulo
                if nuevo_autor: updates["autor"] = nuevo_autor
                if nuevo_genero: updates["genero"] = nuevo_genero
                if nuevo_estado: updates["estado_de_lectura"] = nuevo_estado

                if updates:
                    collection.update_one({"_id": obj_id}, {"$set": updates})
                    print("¡Libro actualizado correctamente!")
                else:
                    print("No se realizaron cambios.")

            elif opcion == "3":
                print("\n--- Eliminar Libro ---")
                libros = list(collection.find())
                if not libros:
                    print("No hay libros registrados.")
                    continue

                for l in libros:
                    print(f"ID: {l['_id']} | Título: {l['titulo']}")
                
                libro_id_str = input("\nIngresa el ID del libro a eliminar: ").strip()
                
                try:
                    obj_id = ObjectId(libro_id_str)
                except Exception:
                    print("Error: El ID ingresado no es válido.")
                    continue

                resultado = collection.delete_one({"_id": obj_id})
                if resultado.deleted_count > 0:
                    print("¡Libro eliminado con éxito de la colección!")
                else:
                    print("No se encontró ningún libro con ese ID.")

            elif opcion == "4":
                print("\n--- Listado de Libros (MongoDB) ---")
                libros = list(collection.find())
                if not libros:
                    print("No hay libros registrados en la base de datos.")
                else:
                    for l in libros:
                        print(f"ID: {l['_id']} | Título: {l.get('titulo')} | Autor: {l.get('autor')} | Género: {l.get('genero')} | Estado: {l.get('estado_de_lectura')}")

            elif opcion == "5":
                print("\n--- Buscar Libros ---")
                criterio = input("Introduce texto para buscar por título, autor o género: ").strip()
                if not criterio:
                    print("El campo de búsqueda no puede estar vacío.")
                    continue

                resultados = list(collection.find({
                    "$or": [
                        {"titulo": {"$regex": criterio, "$options": "i"}},
                        {"autor": {"$regex": criterio, "$options": "i"}},
                        {"genero": {"$regex": criterio, "$options": "i"}}
                    ]
                }))

                if not resultados:
                    print(f"No se encontraron coincidencias para '{criterio}'.")
                else:
                    print(f"\nSe encontraron {len(resultados)} resultados:")
                    for l in resultados:
                        print(f"ID: {l['_id']} | Título: {l.get('titulo')} | Autor: {l.get('autor')} | Género: {l.get('genero')} | Estado: {l.get('estado_de_lectura')}")

            elif opcion == "6":
                print("\nSaliendo del programa. ¡Hasta luego!")
                if client:
                    client.close()
                break
            else:
                print("Opción no válida. Elige un número entre 1 y 6.")

        except PyMongoError as e:
            print(f"Ocurrió un error en la base de datos MongoDB: {e}")
        except Exception as ex:
            print(f"Ocurrió un error inesperado: {ex}")

if __name__ == "__main__":
    menu()