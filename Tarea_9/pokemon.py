import requests
from collections import Counter

BASE_URL = "https://pokeapi.co/api/v2"

# Cache para evitar repetir peticiones a la API y hacer el programa mas rapido
cache = {}

def get_data(url):
    """Realiza peticiones HTTP manejando errores y guardando en cache."""
    if not url.startswith("http"):
        url = f"{BASE_URL}/{url}"
        
    if url in cache:
        return cache[url]
        
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        cache[url] = data
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar {url}: {e}")
        return None

def obtener_todos_paginados(endpoint):
    """Maneja la paginacion de la PokeAPI para traer listas completas."""
    resultados = []
    url = f"{BASE_URL}/{endpoint}?limit=200"
    
    while url:
        data = get_data(url)
        if not data:
            break
        resultados.extend(data.get("results", []))
        url = data.get("next")
    return resultados

# ==========================================
# 1. CLASIFICACION POR TIPOS
# ==========================================
def seccion_tipos():
    print("\n--- 1. CLASIFICACION POR TIPOS ---")
    
    # a) Fuego en Kanto (IDs 1 al 151)
    fuego_data = get_data("type/fire")
    fuego_kanto = []
    if fuego_data:
        for item in fuego_data["pokemon"]:
            poke_id = int(item["pokemon"]["url"].rstrip("/").split("/")[-1])
            if 1 <= poke_id <= 151:
                fuego_kanto.append(item["pokemon"]["name"])
    print(f"a) Pokemon tipo Fuego en Kanto ({len(fuego_kanto)}): {', '.join(fuego_kanto)}")

    # b) Agua con altura > 10 (10 dm = 1 metro)
    agua_data = get_data("type/water")
    agua_altos = []
    if agua_data:
        print("b) Buscando Pokemon de Agua con altura > 10 dm (esto toma unos segundos)...")
        for item in agua_data["pokemon"]:
            detalles = get_data(item["pokemon"]["url"])
            if detalles and detalles.get("height", 0) > 10:
                agua_altos.append(f"{detalles['name']} ({detalles['height']} dm)")
    print(f"   Encontrados ({len(agua_altos)}): {', '.join(agua_altos[:15])} ... [Mostrando primeros 15]")

# ==========================================
# 2. EVOLUCIONES
# ==========================================
def seccion_evoluciones():
    print("\n--- 2. EVOLUCIONES ---")
    
    # a) Cadena evolutiva de un inicial (Ej: Bulbasaur)
    inicial = "bulbasaur"
    especie = get_data(f"pokemon-species/{inicial}")
    if especie and especie.get("evolution_chain"):
        cadena_data = get_data(especie["evolution_chain"]["url"])
        
        def recorrer_cadena(nodo):
            nombres = [nodo["species"]["name"]]
            for evo in nodo.get("evolves_to", []):
                nombres.extend(recorrer_cadena(evo))
            return nombres
            
        evoluciones = recorrer_cadena(cadena_data["chain"])
        print(f"a) Cadena evolutiva de {inicial.capitalize()}: {' -> '.join(evoluciones)}")

    # b) Electricos sin evoluciones (ni pre-evoluciones)
    elec_data = get_data("type/electric")
    sin_evolucion = []
    if elec_data:
        for item in elec_data["pokemon"]:
            poke_detalles = get_data(item["pokemon"]["url"])
            if not poke_detalles:
                continue
            sp_data = get_data(poke_detalles["species"]["url"])
            if sp_data and sp_data.get("evolves_from_species") is None:
                evo_chain = get_data(sp_data["evolution_chain"]["url"])
                if evo_chain and len(evo_chain["chain"]["evolves_to"]) == 0:
                    sin_evolucion.append(sp_data["name"])
                    
    sin_evolucion_unicos = sorted(list(set(sin_evolucion)))
    print(f"b) Pokemon Electricos sin evoluciones: {', '.join(sin_evolucion_unicos)}")

# ==========================================
# 3. ESTADISTICAS DE BATALLA
# ==========================================
def seccion_estadisticas():
    print("\n--- 3. ESTADISTICAS DE BATALLA ---")
    
    # a) Mayor ataque base en Johto (IDs 152 al 251)
    max_ataque = -1
    poke_fuerte = ""
    for pid in range(152, 252):
        p_data = get_data(f"pokemon/{pid}")
        if p_data:
            for s in p_data["stats"]:
                if s["stat"]["name"] == "attack" and s["base_stat"] > max_ataque:
                    max_ataque = s["base_stat"]
                    poke_fuerte = p_data["name"]
    print(f"a) Mayor ataque en Johto: {poke_fuerte.capitalize()} ({max_ataque})")

    # b) Mayor velocidad que NO sea legendario ni singular
    print("b) Analizando velocidades en toda la Pokedex (tomara un momento)...")
    todos = obtener_todos_paginados("pokemon")
    max_vel = -1
    poke_rapido = ""
    
    for p in todos:
        p_data = get_data(p["url"])
        if not p_data:
            continue
        sp_data = get_data(p_data["species"]["url"])
        if sp_data and not sp_data.get("is_legendary") and not sp_data.get("is_mythical"):
            for s in p_data["stats"]:
                if s["stat"]["name"] == "speed" and s["base_stat"] > max_vel:
                    max_vel = s["base_stat"]
                    poke_rapido = p_data["name"]
                    
    print(f"   Mas rapido no legendario/singular: {poke_rapido.capitalize()} ({max_vel})")

# ==========================================
# 4. EXTRAS
# ==========================================
def seccion_extras():
    print("\n--- 4. EXTRAS ---")
    
    # a) Habitat mas comun en tipo Planta
    planta_data = get_data("type/grass")
    habitats = []
    if planta_data:
        for item in planta_data["pokemon"]:
            p_detalles = get_data(item["pokemon"]["url"])
            if p_detalles:
                sp_data = get_data(p_detalles["species"]["url"])
                if sp_data and sp_data.get("habitat"):
                    habitats.append(sp_data["habitat"]["name"])
                    
    if habitats:
        comun, cant = Counter(habitats).most_common(1)[0]
        print(f"a) Habitat mas comun en tipo Planta: '{comun}' ({cant} Pokemon)")

    # b) Menor peso registrado en toda la API
    todos = obtener_todos_paginados("pokemon")
    min_peso = float("inf")
    ligeros = []
    
    for p in todos:
        p_data = get_data(p["url"])
        if p_data and p_data.get("weight") is not None:
            peso = p_data["weight"]
            if peso < min_peso:
                min_peso = peso
                ligeros = [p_data["name"]]
            elif peso == min_peso:
                ligeros.append(p_data["name"])
                
    print(f"b) Menor peso registrado: {min_peso} hg ({min_peso/10} kg) -> {', '.join(ligeros)}")

# Ejecutar todo el programa
if __name__ == "__main__":
    print("Iniciando consultas a la PokeAPI...")
    seccion_tipos()
    seccion_evoluciones()
    seccion_estadisticas()
    seccion_extras()
    print("\nTarea completada con exito.")