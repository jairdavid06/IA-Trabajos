import time
from collections import deque
from itertools import zip_longest
# Representación del estado: (misioneros_izquierda, canibales_izquierda, bote_en_izquierda)
# posicion_bote: 1 si el bote está en la orilla izquierda, 0 si está en la orilla derecha
ESTADO_INICIAL = (3, 3, 1)
ESTADO_OBJETIVO = (0, 0, 0)

# Capacidad máxima del bote: 2 personas (debe ir al menos 1 remando)
# Formato de cada acción permitida: (cantidad_misioneros, cantidad_canibales)
MOVIMIENTOS_PERMITIDOS_BOTE = [
    (1, 0),  # Transportar 1 misionero
    (2, 0),  # Transportar 2 misioneros
    (0, 1),  # Transportar 1 caníbal
    (0, 2),  # Transportar 2 caníbales
    (1, 1)   # Transportar 1 misionero y 1 caníbal
]

def es_orilla_segura(misioneros: int, canibales: int) -> bool:
    """
    Verifica la regla de seguridad en una orilla específica:
    Si hay misioneros presentes en la orilla (misioneros > 0), su número no puede 
    ser superado por el de los caníbales para evitar que sean devorados.
    """
    if misioneros == 0:
        return True  # Si no hay misioneros, los caníbales no representan peligro
    return misioneros >= canibales

def es_estado_valido(estado: tuple[int, int, int]) -> bool:
    """
    Evalúa si un estado global del sistema respeta los límites poblacionales 
    y las condiciones de seguridad en ambas orillas del río.
    """
    misioneros_izq, canibales_izq, posicion_bote = estado
    
    # Validar rangos físicos permitidos en la orilla izquierda (0 a 3) y estado del bote (0 o 1)
    if not (0 <= misioneros_izq <= 3) or not (0 <= canibales_izq <= 3) or posicion_bote not in (0, 1):
        return False
        
    # Calcular la población remanente en la orilla derecha
    misioneros_der = 3 - misioneros_izq
    canibales_der = 3 - canibales_izq
    
    # Comprobar la seguridad tanto en la orilla izquierda como en la derecha
    return es_orilla_segura(misioneros_izq, canibales_izq) and es_orilla_segura(misioneros_der, canibales_der)

def obtener_sucesores(estado: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """
    Genera todos los estados sucesores válidos a partir del estado actual,
    simulando el viaje del bote de una orilla a otra según los movimientos permitidos.
    """
    misioneros_izq, canibales_izq, posicion_bote = estado
    estados_sucesores = []
    
    for misioneros_viaje, canibales_viaje in MOVIMIENTOS_PERMITIDOS_BOTE:
        if posicion_bote == 1:  # El bote está en la izquierda y viaja hacia la derecha
            # Verificar que hay suficientes personas en la orilla izquierda para realizar el viaje
            if misioneros_viaje <= misioneros_izq and canibales_viaje <= canibales_izq:
                nuevo_estado = (
                    misioneros_izq - misioneros_viaje,
                    canibales_izq - canibales_viaje,
                    0  # El bote llega a la orilla derecha
                )
                if es_estado_valido(nuevo_estado):
                    estados_sucesores.append(nuevo_estado)
        else:  # El bote está en la derecha y viaja hacia la izquierda
            misioneros_der = 3 - misioneros_izq
            canibales_der = 3 - canibales_izq
            # Verificar que hay suficientes personas en la orilla derecha para realizar el viaje
            if misioneros_viaje <= misioneros_der and canibales_viaje <= canibales_der:
                nuevo_estado = (
                    misioneros_izq + misioneros_viaje,
                    canibales_izq + canibales_viaje,
                    1  # El bote llega a la orilla izquierda
                )
                if es_estado_valido(nuevo_estado):
                    estados_sucesores.append(nuevo_estado)
                    
    return estados_sucesores


def bfs(inicial, objetivo):
    cola = deque([inicial])  # Cola para BFS
    visitados = set([inicial])  # Conjunto para estados visitados
    padre = {inicial: None}  # Diccionario para rastrear el camino
    nodos_expandidos = 0    
    
    while cola:  # Mientras haya estados en la cola
        estado = cola.popleft()  
        if estado == objetivo:
            break
        nodos_expandidos += 1
        for sucesor in obtener_sucesores(estado):  # Obtener sucesores del estado actual
            if sucesor not in visitados:  # Si el sucesor no ha sido visitado
                visitados.add(sucesor)
                cola.append(sucesor)
                padre[sucesor] = estado
                
    existe_ruta = objetivo in padre  # Verificar si se encontró una ruta al objetivo
    ruta = []
    if existe_ruta:
        actual = objetivo
        while actual is not None:  # Reconstruir la ruta desde el objetivo hasta el inicio
            ruta.append(actual)
            actual = padre[actual]
        ruta.reverse()
        
    return existe_ruta, ruta, nodos_expandidos, len(visitados)

def dfs(inicio, objetivo):
    pila = [inicio]  # Pila para DFS
    visitados = {inicio}  # Conjunto para estados visitados
    padre = {inicio: None}  # Diccionario para rastrear el camino
    nodos_expandidos = 0
    
    while pila:  # Mientras haya estados en la pila
        estado = pila.pop()
        if estado == objetivo:
            break
        nodos_expandidos += 1
        for sucesor in obtener_sucesores(estado):  # Obtener sucesores del estado actual
            if sucesor not in visitados:  # Si el sucesor no ha sido visitado
                visitados.add(sucesor)
                pila.append(sucesor)
                padre[sucesor] = estado
                
    existe_ruta = objetivo in padre  # Verificar si se encontró una ruta al objetivo
    ruta = []
    if existe_ruta:
        actual = objetivo
        while actual is not None:  # Reconstruir la ruta desde el objetivo hasta el inicio
            ruta.append(actual)
            actual = padre[actual]
        ruta.reverse()
        
    return existe_ruta, ruta, nodos_expandidos, len(visitados)

def calcular_factor_ramificacion_efectivo(nodos_totales: int, profundidad: int) -> float:
    if profundidad <= 0 or nodos_totales <= 1:
        return 0.0
        
    def evaluar_arbol(b):
        if b == 1.0:
            return float(profundidad + 1)
        return sum(b**i for i in range(profundidad + 1))

    # Búsqueda binaria para b* entre 0.0 y nodos_totales
    low, high = 0.0, float(nodos_totales)
    for _ in range(50):
        mid = (low + high) / 2.0
        if evaluar_arbol(mid) < nodos_totales:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0

def ejecutar_benchmark():
    print(f"{'Benchmark DFS y BFS':^77}")
    print("-" * 79)
    
    # BFS 
    t_inicio = time.perf_counter()
    exito_bfs, ruta_bfs, exp_bfs, vis_bfs = bfs(ESTADO_INICIAL, ESTADO_OBJETIVO)
    tiempo_bfs = time.perf_counter() - t_inicio
    profundidad_bfs = len(ruta_bfs) - 1 if exito_bfs else 0
    b_estrella_bfs = calcular_factor_ramificacion_efectivo(vis_bfs, profundidad_bfs)
    
    # DFS 
    t_inicio = time.perf_counter()
    exito_dfs, ruta_dfs, exp_dfs, vis_dfs = dfs(ESTADO_INICIAL, ESTADO_OBJETIVO)
    tiempo_dfs = time.perf_counter() - t_inicio
    profundidad_dfs = len(ruta_dfs) - 1 if exito_dfs else 0
    b_estrella_dfs = calcular_factor_ramificacion_efectivo(vis_dfs, profundidad_dfs)
    
    # Despliegue de Resultados en Tabla 
    print(f"{'Métrica Evaluada':<32} | {'BFS (Anchura)':<20} | {'DFS (Profundidad)':<20}")
    print("-" * 79)
    print(f"{'Solución Encontrada':<32} | {'Sí (' + str(profundidad_bfs) + ' pasos)' if exito_bfs else 'No':<20} | {'Sí (' + str(profundidad_dfs) + ' pasos)' if exito_dfs else 'No':<20}")
    print(f"{'Nodos Expandidos':<32} | {exp_bfs:<20} | {exp_dfs:<20}")
    print(f"{'Estados Descubiertos (Memoria)':<32} | {vis_bfs:<20} | {vis_dfs:<20}")
    print(f"{'Tiempo de Ejecución (s)':<32} | {tiempo_bfs:.7f} s           | {tiempo_dfs:.7f} s")
    print(f"{'Factor de Ramificación (b*)':<32} | {b_estrella_bfs:.4f}               | {b_estrella_dfs:.4f}")
    
    print("\n" + f"{'Comparativa de Caminos (BFS vs DFS)':^79}")
    print(f"{'Paso':<8} | {'Camino BFS':<32} | {'Camino DFS':<32}")
    print("-" * 79)
    
    for idx, (paso_bfs, paso_dfs) in enumerate(zip_longest(ruta_bfs, ruta_dfs, fillvalue=None)):
        str_bfs = str(paso_bfs) if paso_bfs is not None else "--- (Meta alcanzada)"
        str_dfs = str(paso_dfs) if paso_dfs is not None else "--- (Meta alcanzada)"
        
        print(f"{idx:<8} | {str_bfs:<32} | {str_dfs:<32}")
    print("-" * 79)

    
if __name__ == "__main__":
    ejecutar_benchmark()