RESET = "\033[0m"
GRIS = "\033[90m"
VERDE = "\033[92m"
AZUL = "\033[94m"
ROJO = "\033[91m"
MORADO = "\033[95m"
FONDO_VERDE = "\033[42m\033[30m"


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


def imprimir_leyenda():
    print(f"\n{AZUL}S{RESET} inicio   {ROJO}E{RESET} final   "
          f"{MORADO}P{RESET} portal   {VERDE}(){RESET} camino   "
          f"{FONDO_VERDE}P {RESET} portal usado")


def pedir_entero(mensaje, defecto, minimo, maximo):
    texto = input(f"{mensaje} [{defecto}]: ").strip()
    if texto == "":
        return defecto
    if texto.lstrip("-").isdigit() and minimo <= int(texto) <= maximo:
        return int(texto)
    print(f"  Escribe un numero entre {minimo} y {maximo}.")
    return pedir_entero(mensaje, defecto, minimo, maximo)
