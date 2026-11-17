"""
Laberinto N x M con portales - U2_T2
=====================================
Reglas del proyecto:
  - El laberinto se genera automaticamente a partir de una seed.
  - Se busca el camino mas corto del inicio (S) al final (E).
  - Hay 3 portales "P" en posiciones aleatorias. Cada uno tiene un salto
    (x, y) aleatorio y manda al personaje a la casilla (p+x, p+y).
    El salto se valida al generar: el destino siempre queda dentro del
    laberinto y en una casilla libre.
  - NO se usan ciclos (for / while): todo se recorre con recursividad.
  - NO se usan algoritmos de busqueda conocidos (BFS, Dijkstra, A*).
  - El laberinto se resuelve con UNA sola funcion recursiva: resolver().
  - La PILA que recorre el laberinto es la pila de llamadas de la
    recursion: cada llamada es una casilla apilada y cada return la desapila.
  - NO se usan estructuras auxiliares: toda la informacion (paredes,
    portales, casillas visitadas y el camino final) vive en la misma matriz.

Codigos de cada casilla de la matriz:
  '#'          pared
  'L'          libre
  'S'          inicio
  'E'          final
  'P,dx,dy'    portal (dx = salto en columnas, dy = salto en filas)
  Una letra en minuscula ('l', 's', 'p,dx,dy') significa que la casilla
  esta visitada en el camino actual. Al terminar, las que quedan en
  minuscula forman el camino mas corto.
"""

import os
import random
import sys
import threading

INF = float("inf")
DIRECCIONES = ((-1, 0), (1, 0), (0, -1), (0, 1))  # arriba, abajo, izquierda, derecha

# Colores ANSI para la consola
RESET = "\033[0m"
GRIS = "\033[90m"
VERDE = "\033[92m"
AZUL = "\033[94m"
ROJO = "\033[91m"
MORADO = "\033[95m"
FONDO_VERDE = "\033[42m\033[30m"


# ----------------------------------------------------------------------
# 1. GENERACION DEL LABERINTO
# ----------------------------------------------------------------------

def crear_matriz(filas, columnas):
    """Crea una matriz llena de paredes, fila por fila, de forma recursiva."""
    if filas == 0:
        return []
    return [["#"] * columnas] + crear_matriz(filas - 1, columnas)


def excavar(lab, f, c):
    """Abre la casilla (f, c) y excava hacia sus vecinos en orden aleatorio."""
    lab[f][c] = "L"
    orden = random.sample(DIRECCIONES, 4)
    probar_direccion(lab, f, c, orden, 0)


def probar_direccion(lab, f, c, orden, i):
    """Prueba la direccion i; si la casilla a 2 pasos sigue cerrada, tumba la
    pared de en medio y sigue excavando desde ahi. Luego prueba la siguiente."""
    if i == 4:
        return
    df, dc = orden[i]
    nf, nc = f + 2 * df, c + 2 * dc
    if 0 < nf < len(lab) - 1 and 0 < nc < len(lab[0]) - 1 and lab[nf][nc] == "#":
        lab[f + df][c + dc] = "L"
        excavar(lab, nf, nc)
    probar_direccion(lab, f, c, orden, i + 1)


def salto_valido(lab, f, c):
    """Genera un salto (dx, dy) aleatorio hasta que el destino sea valido:
    dentro del laberinto y en una casilla libre (no pared, no S, no E,
    no otro portal)."""
    dx = random.randint(-(len(lab[0]) - 1), len(lab[0]) - 1)
    dy = random.randint(-(len(lab) - 1), len(lab) - 1)
    nf, nc = f + dy, c + dx
    if (dx, dy) != (0, 0) and 0 <= nf < len(lab) and 0 <= nc < len(lab[0]) and lab[nf][nc] == "L":
        return dx, dy
    return salto_valido(lab, f, c)


def colocar_portales(lab, faltan, numero=1):
    """Coloca los portales en casillas libres al azar.
    Primero reserva TODAS las posiciones (bajando en la recursion) y despues,
    al regresar, le asigna a cada uno su salto. Asi ningun salto cae encima
    de otro portal."""
    if faltan == 0:
        return
    f = random.randrange(1, len(lab) - 1)
    c = random.randrange(1, len(lab[0]) - 1)
    if lab[f][c] != "L":
        colocar_portales(lab, faltan, numero)  # casilla ocupada: intentar otra
        return
    lab[f][c] = "P,0,0"  # reservar el lugar
    colocar_portales(lab, faltan - 1, numero + 1)
    dx, dy = salto_valido(lab, f, c)
    lab[f][c] = f"P,{dx},{dy}"
    print(f"  Portal {numero}: casilla ({c},{f})  salto x={dx:+d}, y={dy:+d}"
          f"  ->  destino ({c + dx},{f + dy})")


def generar_laberinto(n, m, seed, num_portales=3):
    """Genera un laberinto de n x m celdas (matriz de (2n+1) x (2m+1))."""
    random.seed(seed)
    lab = crear_matriz(2 * n + 1, 2 * m + 1)
    excavar(lab, 1, 1)
    lab[1][1] = "S"
    lab[2 * n - 1][2 * m - 1] = "E"
    print("\nPortales generados:")
    colocar_portales(lab, num_portales)
    return lab


# ----------------------------------------------------------------------
# 2. RESOLUCION (UNA SOLA FUNCION RECURSIVA)
# ----------------------------------------------------------------------

def resolver(lab, f, c, pasos, limite, dejar_camino):
    """Busca el camino mas corto desde (f, c) hasta E.

    - pasos: pasos dados hasta llegar aqui.
    - limite: no se exploran caminos de 'limite' pasos o mas.
    - dejar_camino:
        False -> explora TODO y regresa la menor cantidad de pasos.
        True  -> se detiene en el primer camino que llega a E y deja sus
                 casillas marcadas en la matriz (ese es el camino mas corto).

    La pila de llamadas funciona como la PILA del recorrido: entrar a una
    casilla = push (marcarla), regresar = pop (desmarcarla).
    """
    if pasos >= limite:
        return INF
    celda = lab[f][c]
    tipo = celda[0]
    if tipo == "E":
        return pasos
    if tipo == "#" or tipo.islower():  # pared o ya esta en el camino actual
        return INF

    lab[f][c] = tipo.lower() + celda[1:]  # PUSH: marcar como visitada

    arriba = resolver(lab, f - 1, c, pasos + 1, limite, dejar_camino)
    if dejar_camino and arriba < INF:
        return arriba
    abajo = resolver(lab, f + 1, c, pasos + 1, limite, dejar_camino)
    if dejar_camino and abajo < INF:
        return abajo
    izquierda = resolver(lab, f, c - 1, pasos + 1, limite, dejar_camino)
    if dejar_camino and izquierda < INF:
        return izquierda
    derecha = resolver(lab, f, c + 1, pasos + 1, limite, dejar_camino)
    if dejar_camino and derecha < INF:
        return derecha

    portal = INF
    if tipo == "P":  # el portal es una opcion mas: saltar a (p+x, p+y)
        _, dx, dy = celda.split(",")
        portal = resolver(lab, f + int(dy), c + int(dx), pasos + 1, limite, dejar_camino)
        if dejar_camino and portal < INF:
            return portal

    lab[f][c] = celda  # POP: desmarcar al regresar
    return min(arriba, abajo, izquierda, derecha, portal)


# ----------------------------------------------------------------------
# 3. IMPRESION
# ----------------------------------------------------------------------

def simbolo(celda):
    tipo = celda[0]
    if tipo == "#":
        return GRIS + "██" + RESET
    if tipo == "L":
        return "  "
    if tipo == "l":
        return VERDE + "()" + RESET
    if tipo in "Ss":
        return AZUL + "S " + RESET
    if tipo == "E":
        return ROJO + "E " + RESET
    if tipo == "P":
        return MORADO + "P " + RESET
    if tipo == "p":
        return FONDO_VERDE + "P " + RESET
    return "??"


def imprimir(lab, f=0):
    if f == len(lab):
        return
    print("".join(map(simbolo, lab[f])))
    imprimir(lab, f + 1)


# ----------------------------------------------------------------------
# 4. PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------

def pedir_entero(mensaje, defecto, minimo, maximo):
    texto = input(f"{mensaje} [{defecto}]: ").strip()
    if texto == "":
        return defecto
    if texto.lstrip("-").isdigit() and minimo <= int(texto) <= maximo:
        return int(texto)
    print(f"  Escribe un numero entre {minimo} y {maximo}.")
    return pedir_entero(mensaje, defecto, minimo, maximo)


def main():
    os.system("")  # activa los colores en la terminal de Windows
    print("=== LABERINTO CON PORTALES ===")
    n = pedir_entero("Filas (N)", 10, 3, 40)
    m = pedir_entero("Columnas (M)", 15, 3, 40)
    seed = pedir_entero("Seed (misma seed = mismo laberinto)",
                        random.randint(1, 99999), 0, 10**9)
    print(f"\nUsando seed: {seed}")

    lab = generar_laberinto(n, m, seed)

    print("\nLaberinto generado:")
    imprimir(lab)

    mejor = resolver(lab, 1, 1, 0, INF, False)
    if mejor == INF:
        print("\nNo existe camino de S a E.")
        return
    resolver(lab, 1, 1, 0, mejor + 1, True)

    print(f"\nCamino mas corto: {mejor} pasos")
    imprimir(lab)
    print(f"\n{AZUL}S{RESET} inicio   {ROJO}E{RESET} final   "
          f"{MORADO}P{RESET} portal   {VERDE}(){RESET} camino   "
          f"{FONDO_VERDE}P {RESET} portal usado")


if __name__ == "__main__":
    # La recursion puede ser profunda en laberintos grandes: se sube el limite
    # y se corre en un hilo con mas memoria de pila.
    sys.setrecursionlimit(100000)
    threading.stack_size(64 * 1024 * 1024)
    hilo = threading.Thread(target=main)
    hilo.start()
    hilo.join()