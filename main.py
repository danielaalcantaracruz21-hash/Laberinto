import os
import random
import sys
import threading
from generador import generar_laberinto
from pantalla import imprimir, imprimir_leyenda, pedir_entero
from resolver import INF, resolver
def main():
    os.system("")  
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
    imprimir_leyenda()


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    threading.stack_size(64 * 1024 * 1024)
    hilo = threading.Thread(target=main)
    hilo.start()
    hilo.join()
