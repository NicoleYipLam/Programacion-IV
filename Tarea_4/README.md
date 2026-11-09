# Aplicación de Biblioteca Personal con MongoDB (Tarea 4)

Sistema de gestión de biblioteca personal desarrollado en Python, migrado de una base de datos relacional a una base de datos NoSQL basada en documentos JSON utilizando **MongoDB** y el cliente oficial **PyMongo**.

## Requisitos del Sistema
- macOS
- Python 3.x
- Docker Desktop

---

##  Instrucciones para instalar y configurar MongoDB
. Ejecuta el siguiente comando en tu terminal para iniciar un contenedor oficial de MongoDB:
   ```bash
   docker run --name mi-mongo -p 27017:27017 -d mongo:latest
. Instalación de Dependencias
Abre la terminal en la carpeta del proyecto e instala la librería con:
Bash
python3 -m pip install -r requirements.txt
. Comando para Ejecutar la Aplicación
Para iniciar el sistema interactivo NoSQL desde la terminal, ejecuta:
Bash
python3 main.py
. Estructura esperada del Documento JSON en MongoDB
Cada libro se almacena de forma flexible en la colección libros dentro de la base de datos biblioteca_db con los siguientes campos:
JSON
{
  "_id": "ObjectId('65f...')",
  "titulo": "Ejemplo de Título",
  "autor": "Nombre del Autor",
  "genero": "Género literario",
  "estado_de_lectura": "Leído"
}