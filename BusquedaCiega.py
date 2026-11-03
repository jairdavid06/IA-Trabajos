from collections import deque
import time
# Representación del estado: (misioneros_izq, canibales_izq, posicion_bote)
# Posición del bote: 1 = Orilla Izquierda, 0 = Orilla Derecha
ESTADO_INICIAL = (3, 3, 1)
ESTADO_OBJETIVO = (0, 0, 0)

# Acciones permitidas basadas en la capacidad del bote (máximo 2 personas, mínimo 1)
Acciones = [
    (1, 0),  # Mover 1 misionero
    (2, 0),  # Mover 2 misioneros
    (0, 1),  # Mover 1 caníbal
    (0, 2),  # Mover 2 caníbales
    (1, 1)   # Mover 1 misionero y 1 caníbal
]

def es_estado_seguro(estado: tuple[int, int, int]) -> bool:
    """Valida que los caníbales no superen a los misioneros en ninguna de las orillas."""
    m_izq, c_izq, bote = estado
    
    # Comprobación de límites físicos del sistema
    if not (0 <= m_izq <= 3 and 0 <= c_izq <= 3):
        return False
    if bote not in (0, 1):
        return False
        
    # Cálculo de personas en la orilla opuesta (derecha)
    m_der = 3 - m_izq
    c_der = 3 - c_izq
    
    # Restricción en la orilla izquierda: si hay misioneros, no deben ser superados por caníbales
    if 0 < m_izq < c_izq:
        return False
        
    # Restricción en la orilla derecha: si hay misioneros, no deben ser superados por caníbales
    if 0 < m_der < c_der:
        return False
        
    return True

def obtener_sucesores(estado: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """Genera todos los estados sucesores válidos aplicando los operadores de movimiento."""
    sucesores = []
    m_izq, c_izq, bote = estado
    
    for mov_m, mov_c in Acciones:
        if bote == 1:  # El bote está en la izquierda, viaja hacia la derecha
            if mov_m > m_izq or mov_c > c_izq:
                continue
            siguiente_estado = (m_izq - mov_m, c_izq - mov_c, 0)
        else:          # El bote está en la derecha, viaja hacia la izquierda
            m_der = 3 - m_izq
            c_der = 3 - c_izq
            if mov_m > m_der or mov_c > c_der:
                continue
            siguiente_estado = (m_izq + mov_m, c_izq + mov_c, 1)
            
        # Únicamente se agregan los estados que cumplen con las reglas de seguridad
        if es_estado_seguro(siguiente_estado):
            sucesores.append(siguiente_estado)
            
    return sucesores