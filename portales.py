import random
def salto_valido(lab, f, c):
    dx = random.randint(-(len(lab[0]) - 1), len(lab[0]) - 1)
    dy = random.randint(-(len(lab) - 1), len(lab) - 1)
    nf, nc = f + dy, c + dx
    if (dx, dy) != (0, 0) and 0 <= nf < len(lab) and 0 <= nc < len(lab[0]) and lab[nf][nc] == "L":
        return dx, dy
    return salto_valido(lab, f, c)
def colocar_portales(lab, faltan, numero=1):
    if faltan == 0:
        return
    f = random.randrange(1, len(lab) - 1)
    c = random.randrange(1, len(lab[0]) - 1)
    if lab[f][c] != "L":
        colocar_portales(lab, faltan, numero)  
        return
    lab[f][c] = "P,0,0"
    colocar_portales(lab, faltan - 1, numero + 1)
    dx, dy = salto_valido(lab, f, c)
    lab[f][c] = f"P,{dx},{dy}"
    print(f"  Portal {numero}: casilla ({c},{f})  salto x={dx:+d}, y={dy:+d}"
          f"  ->  destino ({c + dx},{f + dy})")
