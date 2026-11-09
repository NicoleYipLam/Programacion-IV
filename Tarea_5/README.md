# Aplicación de Biblioteca Personal con KeyDB (Tarea 5)

Sistema de gestión de biblioteca personal desarrollado en Python, migrado a un almacenamiento en memoria de alto rendimiento utilizando **KeyDB** (compatible con Redis), serialización en formato **JSON** y la librería `redis-py`.

## Requisitos del Sistema
- macOS
- Python 3.x
- Docker Desktop

---

## Configuración del Contenedor KeyDB
Inicia el motor de almacenamiento en memoria ejecutando el siguiente comando en tu terminal:
```bash
docker run --name mi-keydb -p 6379:6379 -d eqalpha/keydb:latest
Configuración de Variables de Entorno (.env)
Crea un archivo llamado .env en la raíz del proyecto con la siguiente estructura de conexión:
Code snippet
KEYDB_HOST=localhost
KEYDB_PORT=6379
KEYDB_PASSWORD=
. Instalación de Dependencias
Instala las librerías necesarias ejecutando en tu terminal:
Bash
python3 -m pip install -r requirements.txt
. Ejecución de la Aplicación
Para iniciar el menú interactivo del sistema, ejecuta:
Bash
python3 main.py
. Estructura de Datos (Clave-Valor)
Cada libro se almacena de forma serializada en formato JSON utilizando claves únicas con el formato libro:<id>, gestionadas mediante un contador autoincremental (libro:contador) para garantizar la eficiencia en las operaciones CRUD.