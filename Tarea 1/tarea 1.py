import os
import sqlite3

# Definir la ruta de la base de datos en la misma carpeta donde corre el script
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DB_PATH = os.path.join(DIRECTORIO_ACTUAL, "gremio_aventureros.db")

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
    """Crea las tablas necesarias si no existen."""
    print(f"📂 Creando/Verificando base de datos en: {DB_PATH}")
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Tabla Héroes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            clase TEXT NOT NULL,
            nivel_experiencia INTEGER NOT NULL CHECK (nivel_experiencia > 0)
        );
    """)

    # Tabla Misiones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            nivel_dificultad INTEGER NOT NULL CHECK (nivel_dificultad BETWEEN 1 AND 10),
            localizacion TEXT NOT NULL,
            recompensa INTEGER NOT NULL CHECK (recompensa >= 0)
        );
    """)

    # Tabla Monstruos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monstruos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            nivel_amenaza INTEGER NOT NULL CHECK (nivel_amenaza BETWEEN 1 AND 10)
        );
    """)

    # Tabla puente: Misiones y Héroes (Muchos a Muchos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones_heroes (
            mision_id INTEGER,
            heroe_id INTEGER,
            PRIMARY KEY (mision_id, heroe_id),
            FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
            FOREIGN KEY (heroe_id) REFERENCES heroes(id) ON DELETE CASCADE
        );
    """)

    # Tabla puente: Misiones y Monstruos (Muchos a Muchos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones_monstruos (
            mision_id INTEGER,
            monstruo_id INTEGER,
            PRIMARY KEY (mision_id, monstruo_id),
            FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
            FOREIGN KEY (monstruo_id) REFERENCES monstruos(id) ON DELETE CASCADE
        );
    """)

    conexion.commit()
    conexion.close()
    print("✅ Base de datos y tablas inicializadas correctamente.")

def insertar_datos_ejemplo():
    """Inserta algunos registros iniciales para poblar el sistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Verificar si ya existen héroes para no duplicar datos
    cursor.execute("SELECT COUNT(*) FROM heroes;")
    if cursor.fetchone()[0] > 0:
        conexion.close()
        print("ℹ️ Los datos de ejemplo ya existían en la base de datos.")
        return

    # Insertar Héroes
    heroes = [
        ("Aragorn", "Guerrero", 8),
        ("Gandalf", "Mago", 10),
        ("Legolas", "Arquero", 7)
    ]
    cursor.executemany("INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?);", heroes)

    # Insertar Misiones
    misiones = [
        ("Defendimiento de la Puerta Oeste", 4, "Minas de Moria", 500),
        ("Caza del Dragón en la Montaña Solitaria", 9, "Erebor", 5000),
        ("Emboscada en el Bosque Negro", 5, "Bosque Negro", 300)
    ]
    cursor.executemany("INSERT INTO misiones (descripcion, nivel_dificultad, localizacion, recompensa) VALUES (?, ?, ?, ?);", misiones)

    # Insertar Monstruos
    monstruos = [
        ("Orco de las Cavernas", "Goblinoid", 3),
        ("Smaug el Terrible", "Dragón", 10),
        ("Araña Gigante", "Bestia", 6)
    ]
    cursor.executemany("INSERT INTO monstruos (nombre, tipo, nivel_amenaza) VALUES (?, ?, ?);", monstruos)

    # Relacionar Héroes con Misiones
    relaciones_heroes = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 3)
    ]
    cursor.executemany("INSERT OR IGNORE INTO misiones_heroes (mision_id, heroe_id) VALUES (?, ?);", relaciones_heroes)

    # Relacionar Misiones con Monstruos
    relaciones_monstruos = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]
    cursor.executemany("INSERT OR IGNORE INTO misiones_monstruos (mision_id, monstruo_id) VALUES (?, ?);", relaciones_monstruos)

    conexion.commit()
    conexion.close()
    print("⚔️ Datos de ejemplo del gremio insertados con éxito.")

def listar_heroes():
    """Muestra todos los héroes registrados."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, clase, nivel_experiencia FROM heroes;")
    print("\n--- 🛡️ LISTA DE HÉROES ---")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Nombre: {row[1]} | Clase: {row[2]} | Nivel: {row[3]}")
    conexion.close()

if __name__ == "__main__":
    # 1. Inicializar la base de datos (imprimirá la ruta exacta en consola)
    inicializar_base_de_datos()
    
    # 2. Rellenar con datos de prueba
    insertar_datos_ejemplo()
    
    # 3. Mostrar resultados
    listar_heroes()
