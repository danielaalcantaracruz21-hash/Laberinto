INF = float("inf")
def resolver(lab, f, c, pasos, limite, dejar_camino):
    if pasos >= limite:
        return INF
    celda = lab[f][c]
    tipo = celda[0]
    if tipo == "E":
        return pasos
    if tipo == "#" or tipo.islower():
        return INF

    lab[f][c] = tipo.lower() + celda[1:]  

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
    if tipo == "P": 
        _, dx, dy = celda.split(",")
        portal = resolver(lab, f + int(dy), c + int(dx), pasos + 1, limite, dejar_camino)
        if dejar_camino and portal < INF:
            return portal

    lab[f][c] = celda  
    return min(arriba, abajo, izquierda, derecha, portal)
