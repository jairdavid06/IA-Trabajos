import time
from collections import deque

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