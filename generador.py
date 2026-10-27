import random

DIRECCIONES = ((-1, 0), (1, 0), (0, -1), (0, 1))  # arriba, abajo, izquierda, derecha


def crear_matriz(filas, columnas):
    if filas == 0:
        return []
    return [["#"] * columnas] + crear_matriz(filas - 1, columnas)


def excavar(lab, f, c):
    lab[f][c] = "L"
    orden = random.sample(DIRECCIONES, 4)
    probar_direccion(lab, f, c, orden, 0)


def probar_direccion(lab, f, c, orden, i):
    if i == 4:
        return
    df, dc = orden[i]
    nf, nc = f + 2 * df, c + 2 * dc
    if 0 < nf < len(lab) - 1 and 0 < nc < len(lab[0]) - 1 and lab[nf][nc] == "#":
        lab[f + df][c + dc] = "L"
        excavar(lab, nf, nc)
    probar_direccion(lab, f, c, orden, i + 1)
def generar_laberinto(n, m, seed):
    random.seed(seed)
    lab = crear_matriz(2 * n + 1, 2 * m + 1)
    excavar(lab, 1, 1)
    lab[1][1] = "S"
    lab[2 * n - 1][2 * m - 1] = "E"
    return lab
