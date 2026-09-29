import os
import sqlite3

# Definir la ruta de la base de datos en la misma carpeta del script
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DB_PATH = os.path.join(DIRECTORIO_ACTUAL, "biblioteca_personal.db")

def conectar_db():
    """Establece la conexión con la base de datos SQLite y activa las claves foráneas."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion
    except sqlite3.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        raise

def inicializar_base_de_datos():
    """Crea la tabla de libros si no existe."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado_lectura TEXT NOT NULL CHECK(estado_lectura IN ('leido', 'no leido'))
        );
    """)
    conexion.commit()
    conexion.close()

def agregar_libro():
    """Permite añadir un nuevo libro al sistema."""
    print("\n--- 📖 AGREGAR NUEVO LIBRO ---")
    titulo = input("Título del libro: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    
    print("Estado de lectura:")
    print("1. Leído")
    print("2. No leído")
    opcion = input("Seleccione una opción (1 o 2): ").strip()
    
    estado_lectura = "leido" if opcion == "1" else "no leido"
    
    if not titulo or not autor or not genero:
        print("❌ Error: Todos los campos son obligatorios.")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO libros (titulo, autor, genero, estado_lectura)
        VALUES (?, ?, ?, ?);
    """, (titulo, autor, genero, estado_lectura))
    conexion.commit()
    conexion.close()
    print("✅ ¡Libro agregado exitosamente!")

def ver_libros():
    """Muestra todos los libros registrados en la base de datos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, autor, genero, estado_lectura FROM libros;")
    libros = cursor.fetchall()
    conexion.close()

    print("\n--- 📚 LISTADO DE LIBROS ---")
    if not libros:
        print("📭 No hay libros registrados en la biblioteca.")
        return

    for libro in libros:
        print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")

def buscar_libros():
    """Permite buscar libros por título, autor o género."""
    print("\n--- 🔍 BUSCAR LIBROS ---")
    print("1. Buscar por Título")
    print("2. Buscar por Autor")
    print("3. Buscar por Género")
    opcion = input("Elija el criterio de búsqueda (1-3): ").strip()

    criterios = {"1": "titulo", "2": "autor", "3": "genero"}
    if opcion not in criterios:
        print("❌ Opción no válida.")
        return

    columna = criterios[opcion]
    termino = input(f"Ingrese el valor a buscar ({columna}): ").strip()

    conexion = conectar_db()
    cursor = conexion.cursor()
    query = f"SELECT id, titulo, autor, genero, estado_lectura FROM libros WHERE {columna} LIKE ?;"
    cursor.execute(query, (f"%{termino}%",))
    resultados = cursor.fetchall()
    conexion.close()

    print(f"\n--- RESULTADOS DE BÚSQUEDA ({len(resultados)}) ---")
    if not resultados:
        print("📭 No se encontraron coincidencias.")
        return

    for libro in resultados:
        print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")

def actualizar_libro():
    """Permite modificar cualquier campo de un libro existente."""
    ver_libros()
    try:
        id_libro = int(input("\nIngrese el ID del libro que desea actualizar: ").strip())
    except ValueError:
        print("❌ Por favor, ingrese un ID válido (número entero).")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, autor, genero, estado_lectura FROM libros WHERE id = ?;", (id_libro,))
    libro = cursor.fetchone()

    if not libro:
        print("❌ No se encontró ningún libro con ese ID.")
        conexion.close()
        return

    print(f"\nEditando libro actual: {libro[1]} de {libro[2]}")
    print("Deje el campo en blanco si no desea modificarlo.")

    nuevo_titulo = input(f"Nuevo título [{libro[1]}]: ").strip() or libro[1]
    nuevo_autor = input(f"Nuevo autor [{libro[2]}]: ").strip() or libro[2]
    nuevo_genero = input(f"Nuevo género [{libro[3]}]: ").strip() or libro[3]
    
    print(f"Estado actual: {libro[4]}. ¿Desea cambiarlo?")
    print("1. Cambiar a 'leido'")
    print("2. Cambiar a 'no leido'")
    print("3. Mantener actual")
    opcion_estado = input("Seleccione una opción (1-3): ").strip()

    if opcion_estado == "1":
        nuevo_estado = "leido"
    elif opcion_estado == "2":
        nuevo_estado = "no leido"
    else:
        nuevo_estado = libro[4]

    cursor.execute("""
        UPDATE libros
        SET titulo = ?, autor = ?, genero = ?, estado_lectura = ?
        WHERE id = ?;
    """, (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, id_libro))
    
    conexion.commit()
    conexion.close()
    print("✅ ¡Libro actualizado correctamente!")

def eliminar_libro():
    """Elimina un libro del sistema utilizando su ID."""
    ver_libros()
    try:
        id_libro = int(input("\nIngrese el ID del libro que desea eliminar: ").strip())
    except ValueError:
        print("❌ Por favor, ingrese un ID válido (número entero).")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo FROM libros WHERE id = ?;", (id_libro,))
    libro = cursor.fetchone()

    if not libro:
        print("❌ No se encontró ningún libro con ese ID.")
        conexion.close()
        return

    confirmacion = input(f"¿Está seguro de eliminar '{libro[1]}' (S/N)?: ").strip().lower()
    if confirmacion == 's':
        cursor.execute("DELETE FROM libros WHERE id = ?;", (id_libro,))
        conexion.commit()
        print("🗑️ Libro eliminado exitosamente.")
    else:
        print("❌ Operación cancelada.")
    
    conexion.close()

def menu():
    """Menú interactivo en consola."""
    inicializar_base_de_datos()
    print(f"📂 Base de datos lista en: {DB_PATH}")

    while True:
        print("\n==============================")
        print("📚 SISTEMA DE BIBLIOTECA PERSONAL")
        print("==============================")
        print("1. Agregar nuevo libro")
        print("2. Ver listado de libros")
        print("3. Buscar libros")
        print("4. Actualizar información de un libro")
        print("5. Eliminar libro")
        print("6. Salir")
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            ver_libros()
        elif opcion == "3":
            buscar_libros()
        elif opcion == "4":
            actualizar_libro()
        elif opcion == "5":
            eliminar_libro()
        elif opcion == "6":
            print("\n👋 ¡Gracias por usar la Biblioteca Personal! Saliendo...")
            break
        else:
            print("❌ Opción inválida. Por favor, elija un número entre 1 y 6.")

if __name__ == "__main__":
    menu()
