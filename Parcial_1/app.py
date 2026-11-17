import json
import os

# Archivo donde se guardarán los datos de forma persistente
ARCHIVO_DATOS = "presupuesto.json"

def cargar_articulos():
    """Carga los artículos desde el archivo JSON si existe."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        print("[Aviso] El archivo de datos estaba corrupto. Se iniciará con una lista vacía.")
        return []

def guardar_articulos(articulos):
    """Guarda la lista actual de artículos en el archivo JSON."""
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(articulos, archivo, indent=4, ensure_ascii=False)
    except IOError:
        print("[Error] No se pudo guardar la información en el archivo.")

def registrar_articulo(articulos):
    """Permite registrar un nuevo artículo validando entradas."""
    print("\n--- Registrar Nuevo Artículo ---")
    nombre = input("Nombre del artículo: ").strip()
    if not nombre:
        print("[Error] El nombre no puede estar vacío.")
        return

    categoria = input("Categoría (ej. Materiales, Servicios, Insumos): ").strip()
    if not categoria:
        categoria = "General"

    # Validación estricta para cantidad (entero positivo)
    while True:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad < 0:
                print("[Error] La cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print("[Error] Ingresa un número entero válido para la cantidad.")

    # Validación estricta para precio unitario (decimal positivo)
    while True:
        try:
            precio_unitario = float(input("Precio unitario: "))
            if precio_unitario < 0:
                print("[Error] El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("[Error] Ingresa un número válido para el precio.")

    descripcion = input("Descripción (opcional): ").strip()

    # Generar un ID único basado en el tamaño o el máximo ID existente
    nuevo_id = max([a["id"] for a in articulos], default=0) + 1

    nuevo_articulo = {
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "descripcion": descripcion
    }

    articulos.append(nuevo_articulo)
    guardar_articulos(articulos)
    print(f"¡Éxito! Artículo '{nombre}' registrado correctamente con ID {nuevo_id}.")

def listar_articulos(articulos):
    """Muestra la lista completa de artículos en formato tabular alineado."""
    if not articulos:
        print("\n[Aviso] No hay artículos registrados en el presupuesto.")
        return

    print("\n" + "="*85)
    print(f"{'ID':<4} | {'NOMBRE':<18} | {'CATEGORÍA':<12} | {'CANT':<6} | {'PRECIO U.':<10} | {'SUBTOTAL':<10}")
    print("="*85)

    total_general = 0
    for a in articulos:
        subtotal = a["cantidad"] * a["precio_unitario"]
        total_general += subtotal
        print(f"{a['id']:<4} | {a['nombre']:<18} | {a['categoria']:<12} | {a['cantidad']:<6} | ${a['precio_unitario']:<9.2f} | ${subtotal:<9.2f}")

    print("="*85)
    print(f"TOTAL GENERAL DEL PRESUPUESTO: ${total_general:.2f}")
    print("="*85)

def buscar_articulos(articulos):
    """Permite buscar artículos por coincidencia en nombre o categoría."""
    if not articulos:
        print("\n[Aviso] No hay artículos para buscar.")
        return

    criterio = input("\nBuscar por (1) Nombre o (2) Categoría?: ").strip()
    termino = input("Escribe el término de búsqueda: ").strip().lower()

    resultados = []
    for a in articulos:
        if criterio == "1" and termino in a["nombre"].lower():
            resultados.append(a)
        elif criterio == "2" and termino in a["categoria"].lower():
            resultados.append(a)
        elif criterio not in ["1", "2"]:
            # Búsqueda general si elige mal o prefiere buscar en ambos
            if termino in a["nombre"].lower() or termino in a["categoria"].lower():
                resultados.append(a)

    if not resultados:
        print(f"\n[Aviso] No se encontraron artículos que coincidan con '{termino}'.")
    else:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        listar_articulos(resultados)

def editar_articulo(articulos):
    """Permite actualizar los campos de un artículo existente por su ID."""
    if not articulos:
        print("\n[Aviso] No hay artículos para editar.")
        return

    listar_articulos(articulos)
    try:
        id_buscar = int(input("\nIngresa el ID del artículo que deseas editar: "))
    except ValueError:
        print("[Error] El ID debe ser un número entero.")
        return

    articulo = next((a for a in articulos if a["id"] == id_buscar), None)
    if not articulo:
        print(f"[Error] No se encontró ningún artículo con el ID {id_buscar}.")
        return

    print(f"\nEditando a: {articulo['nombre']}. (Presiona Enter para dejar el valor actual sin cambios).")

    nuevo_nombre = input(f"Nuevo nombre [{articulo['nombre']}]: ").strip()
    if nuevo_nombre:
        articulo["nombre"] = nuevo_nombre

    nueva_cat = input(f"Nueva categoría [{articulo['categoria']}]: ").strip()
    if nueva_cat:
        articulo["categoria"] = nueva_cat

    nueva_cant_str = input(f"Nueva cantidad [{articulo['cantidad']}]: ").strip()
    if nueva_cant_str:
        try:
            cant = int(nueva_cant_str)
            if cant >= 0:
                articulo["cantidad"] = cant
            else:
                print("[Aviso] Cantidad negativa ignorada, se mantiene la anterior.")
        except ValueError:
            print("[Aviso] Valor inválido, se mantiene la cantidad anterior.")

    nuevo_precio_str = input(f"Nuevo precio unitario [{articulo['precio_unitario']}]: ").strip()
    if nuevo_precio_str:
        try:
            precio = float(nuevo_precio_str)
            if precio >= 0:
                articulo["precio_unitario"] = precio
            else:
                print("[Aviso] Precio negativo ignorado, se mantiene el anterior.")
        except ValueError:
            print("[Aviso] Valor inválido, se mantiene el precio anterior.")

    nueva_desc = input(f"Nueva descripción [{articulo['descripcion']}]: ").strip()
    if nueva_desc != "":
        articulo["descripcion"] = nueva_desc

    guardar_articulos(articulos)
    print("¡Artículo actualizado con éxito!")

def eliminar_articulo(articulos):
    """Elimina un artículo por su ID."""
    if not articulos:
        print("\n[Aviso] No hay artículos para eliminar.")
        return

    listar_articulos(articulos)
    try:
        id_eliminar = int(input("\nIngresa el ID del artículo que deseas eliminar: "))
    except ValueError:
        print("[Error] El ID debe ser un número entero.")
        return

    articulo = next((a for a in articulos if a["id"] == id_eliminar), None)
    if not articulo:
        print(f"[Error] No se encontró ningún artículo con el ID {id_eliminar}.")
        return

    confirmacion = input(f"¿Estás segura de eliminar '{articulo['nombre']}'? (s/n): ").strip().lower()
    if confirmacion == 's':
        articulos.remove(articulo)
        guardar_articulos(articulos)
        print("¡Artículo eliminado correctamente!")
    else:
        print("Operación cancelada.")

def main():
    """Función principal que controla el menú de la aplicación."""
    articulos = cargar_articulos()

    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE REGISTRO DE PRESUPUESTO")
        print("="*40)
        print("1. Registrar un nuevo artículo")
        print("2. Listar todos los artículos")
        print("3. Buscar artículos (por nombre o categoría)")
        print("4. Editar un artículo existente")
        print("5. Eliminar un artículo")
        print("6. Salir")
        print("="*40)

        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            registrar_articulo(articulos)
        elif opcion == "2":
            listar_articulos(articulos)
        elif opcion == "3":
            buscar_articulos(articulos)
        elif opcion == "4":
            editar_articulo(articulos)
        elif opcion == "5":
            eliminar_articulo(articulos)
        elif opcion == "6":
            print("\n¡Gracias por usar el sistema de presupuesto! Saliendo...")
            break
        else:
            print("\n[Error] Opción no válida. Por favor, elige un número entre 1 y 6.")

if __name__ == "__main__":
    main()