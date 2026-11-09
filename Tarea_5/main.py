import os
import json
import redis
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

HOST = os.getenv("KEYDB_HOST", "localhost")
PORT = int(os.getenv("KEYDB_PORT", 6379))
PASSWORD = os.getenv("KEYDB_PASSWORD", None)

# Inicializar la conexión a KeyDB / Redis
try:
    client = redis.Redis(
        host=HOST,
        port=PORT,
        password=PASSWORD if PASSWORD else None,
        decode_responses=True # Permite manejar strings directamente en lugar de bytes
    )
    # Verificar conexión
    client.ping()
    print("¡Conexión exitosa a KeyDB!")
except redis.ConnectionError as e:
    print(f"Error crítico: No se pudo conectar a KeyDB. Detalle: {e}")
    client = None

def menu():
    if client is None:
        print("La aplicación no puede iniciar por un error de conexión con KeyDB.")
        return

    while True:
        print("\n==========================================")
        print("   BIBLIOTECA PERSONAL KEYDB (En Memoria)")
        print("==========================================")
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

                # Generar un ID único autoincremental usando un contador en KeyDB
                nuevo_id = client.incr("libro:contador")
                clave_libro = f"libro:{nuevo_id}"

                libro_data = {
                    "id": str(nuevo_id),
                    "titulo": titulo,
                    "autor": autor,
                    "genero": genero,
                    "estado_de_lectura": estado
                }

                # Guardar en KeyDB usando SET con el objeto serializado en JSON
                client.set(clave_libro, json.dumps(libro_data))
                print(f"¡Libro agregado exitosamente con ID {nuevo_id} (clave: {clave_libro})!")

            elif opcion == "2":
                print("\n--- Actualizar Libro ---")
                claves = [c for c in client.keys("libro:*") if c != "libro:contador"]

                if not claves:
                    print("No hay libros registrados para actualizar.")
                    continue

                for clave in claves:
                    data = json.loads(client.get(clave))
                    print(f"ID: {data['id']} | Título: {data['titulo']} - Autor: {data['autor']}")
                
                libro_id = input("\nIngresa el ID del libro que deseas actualizar: ").strip()
                clave_buscada = f"libro:{libro_id}"

                if not client.exists(clave_buscada):
                    print("No se encontró ningún libro con ese ID.")
                    continue

                libro_actual = json.loads(client.get(clave_buscada))
                print(f"Editando a: {libro_actual['titulo']}. Deja en blanco si no quieres cambiar el dato.")
                
                nuevo_titulo = input(f"Nuevo título [{libro_actual.get('titulo', '')}]: ").strip()
                nuevo_autor = input(f"Nuevo autor [{libro_actual.get('autor', '')}]: ").strip()
                nuevo_genero = input(f"Nuevo género [{libro_actual.get('genero', '')}]: ").strip()
                nuevo_estado = input(f"Nuevo estado [{libro_actual.get('estado_de_lectura', '')}]: ").strip()

                if nuevo_titulo: libro_actual["titulo"] = nuevo_titulo
                if nuevo_autor: libro_actual["autor"] = nuevo_autor
                if nuevo_genero: libro_actual["genero"] = nuevo_genero
                if nuevo_estado: libro_actual["estado_de_lectura"] = nuevo_estado

                # Guardar los cambios actualizados sobre la misma clave
                client.set(clave_buscada, json.dumps(libro_actual))
                print("¡Libro actualizado correctamente en KeyDB!")

            elif opcion == "3":
                print("\n--- Eliminar Libro ---")
                claves = [c for c in client.keys("libro:*") if c != "libro:contador"]
                if not claves:
                    print("No hay libros registrados.")
                    continue

                for clave in claves:
                    data = json.loads(client.get(clave))
                    print(f"ID: {data['id']} | Título: {data['titulo']}")
                
                libro_id = input("\nIngresa el ID del libro a eliminar: ").strip()
                clave_buscada = f"libro:{libro_id}"

                if client.exists(clave_buscada):
                    client.delete(clave_buscada)
                    print("¡Libro eliminado con éxito de KeyDB!")
                else:
                    print("No se encontró ningún libro con ese ID.")

            elif opcion == "4":
                print("\n--- Listado de Libros (KeyDB) ---")
                claves = [c for c in client.keys("libro:*") if c != "libro:contador"]
                if not claves:
                    print("No hay libros registrados en la base de datos.")
                else:
                    for clave in claves:
                        l = json.loads(client.get(clave))
                        print(f"ID: {l.get('id')} | Título: {l.get('titulo')} | Autor: {l.get('autor')} | Género: {l.get('genero')} | Estado: {l.get('estado_de_lectura')}")

            elif opcion == "5":
                print("\n--- Buscar Libros ---")
                criterio = input("Introduce texto para buscar por título, autor o género: ").strip().lower()
                if not criterio:
                    print("El campo de búsqueda no puede estar vacío.")
                    continue

                claves = [c for c in client.keys("libro:*") if c != "libro:contador"]
                resultados = []

                for clave in claves:
                    l = json.loads(client.get(clave))
                    if (criterio in l.get("titulo", "").lower() or 
                        criterio in l.get("autor", "").lower() or 
                        criterio in l.get("genero", "").lower()):
                        resultados.append(l)

                if not resultados:
                    print(f"No se encontraron coincidencias para '{criterio}'.")
                else:
                    print(f"\nSe encontraron {len(resultados)} resultados:")
                    for l in resultados:
                        print(f"ID: {l.get('id')} | Título: {l.get('titulo')} | Autor: {l.get('autor')} | Género: {l.get('genero')} | Estado: {l.get('estado_de_lectura')}")

            elif opcion == "6":
                print("\nSaliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elige un número entre 1 y 6.")

        except redis.RedisError as e:
            print(f"Ocurrió un error en KeyDB: {e}")
        except Exception as ex:
            print(f"Ocurrió un error inesperado: {ex}")

if __name__ == "__main__":
    menu()