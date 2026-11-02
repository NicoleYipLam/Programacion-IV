from database import engine, Base, SessionLocal
from models import Libro

# Crear las tablas automáticamente en MariaDB si no existen
Base.metadata.create_all(bind=engine)

def menu():
    while True:
        print("\n==============================")
        print("   BIBLIOTECA PERSONAL ORM    ")
        print("==============================")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros (Título, Autor o Género)")
        print("6. Salir")
        
        opcion = input("\nElige una opción (1-6): ").strip()
        db = SessionLocal()

        try:
            if opcion == "1":
                print("\n--- Agregar Nuevo Libro ---")
                titulo = input("Título: ")
                autor = input("Autor: ")
                genero = input("Género: ")
                estado = input("Estado de lectura (Pendiente / Leyendo / Leído): ")
                
                nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado_de_lectura=estado)
                db.add(nuevo_libro)
                db.commit()
                print("¡Libro agregado exitosamente!")

            elif opcion == "2":
                print("\n--- Actualizar Libro ---")
                libros = db.query(Libro).all()
                for l in libros:
                    print(f"ID: {l.id} | {l.titulo} - {l.autor}")
                
                libro_id = input("\nIngresa el ID del libro que deseas actualizar: ")
                libro = db.query(Libro).filter_by(id=libro_id).first()
                
                if libro:
                    print(f"Editando a: {libro.titulo}. Deja en blanco si no quieres cambiar el dato.")
                    nuevo_titulo = input(f"Nuevo título [{libro.titulo}]: ")
                    nuevo_autor = input(f"Nuevo autor [{libro.autor}]: ")
                    nuevo_genero = input(f"Nuevo género [{libro.genero}]: ")
                    nuevo_estado = input(f"Nuevo estado [{libro.estado_de_lectura}]: ")
                    
                    if nuevo_titulo: libro.titulo = nuevo_titulo
                    if nuevo_autor: libro.autor = nuevo_autor
                    if nuevo_genero: libro.genero = nuevo_genero
                    if nuevo_estado: libro.estado_de_lectura = nuevo_estado
                    
                    db.commit()
                    print("¡Libro actualizado correctamente!")
                else:
                    print("No se encontró un libro con ese ID.")

            elif opcion == "3":
                print("\n--- Eliminar Libro ---")
                libros = db.query(Libro).all()
                for l in libros:
                    print(f"ID: {l.id} | {l.titulo}")
                
                libro_id = input("\nIngresa el ID del libro a eliminar: ")
                libro = db.query(Libro).filter_by(id=libro_id).first()
                
                if libro:
                    db.delete(libro)
                    db.commit()
                    print("¡Libro eliminado con éxito!")
                else:
                    print("Libro no encontrado.")

            elif opcion == "4":
                print("\n--- Listado de Libros ---")
                libros = db.query(Libro).all()
                if not libros:
                    print("No hay libros registrados.")
                else:
                    for l in libros:
                        print(f"ID: {l.id} | Título: {l.titulo} | Autor: {l.autor} | Género: {l.genero} | Estado: {l.estado_de_lectura}")

            elif opcion == "5":
                print("\n--- Buscar Libros ---")
                criterio = input("Introduce parte del título, autor o género a buscar: ").strip()
                resultados = db.query(Libro).filter(
                    (Libro.titulo.ilike(f"%{criterio}%")) | 
                    (Libro.autor.ilike(f"%{criterio}%")) | 
                    (Libro.genero.ilike(f"%{criterio}%"))
                ).all()
                
                if not resultados:
                    print("No se encontraron coincidencias.")
                else:
                    print(f"\nSe encontraron {len(resultados)} resultados:")
                    for l in resultados:
                        print(f"ID: {l.id} | Título: {l.titulo} | Autor: {l.autor} | Género: {l.genero} | Estado: {l.estado_de_lectura}")

            elif opcion == "6":
                print("\nSaliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elige un número entre 1 y 6.")

        except Exception as e:
            db.rollback()
            print(f"Ocurrió un error en la base de datos: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    menu()