# Aplicación de Biblioteca Personal con MariaDB y SQLAlchemy

Proyecto desarrollado en Python que migra el almacenamiento tradicional a una base de datos relacional **MariaDB** utilizando **SQLAlchemy ORM**.

## Requisitos del Sistema
- macOS (Apple Silicon / Intel)
- Python 3.x
- Docker Desktop

---

## 1. Instrucciones para instalar y configurar MariaDB (Vía Docker)
1. Instala y abre **Docker Desktop** en tu equipo.
2. Abre la terminal y ejecuta el siguiente comando para correr el contenedor oficial de MariaDB:
   ```bash
   docker run --name mi-mariadb -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=biblioteca_db -p 3307:3306 -d mariadb:latest
2. Configuración de la Cadena de Conexión
La aplicación se conecta mediante SQLAlchemy utilizando la siguiente URI en el archivo database.py:
Python
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3307/biblioteca_db"
3. Instalación de Dependencias
Abre la terminal en la carpeta del proyecto e instala los requerimientos:
Bash
python3 -m pip install -r requirements.txt
4. Comando para Ejecutar la Aplicación
Para iniciar el sistema interactivo de la biblioteca, ejecuta:
Bash
python3 main.py