import heapq
import math
from colorama import init, Fore, Style

# Inicializar colorama
init()

def crear_matriz(tamano):
    # Crear una matriz de tamaño especificado llena de puntos
    matriz = [["[]" for _ in range(tamano)] for _ in range(tamano)]
    return matriz

def imprimir_matriz(matriz):
    # Imprimir los números de columna
    tamano = len(matriz)
    encabezado_columnas = "  " + " ".join(str(i) for i in range(tamano))
    print(encabezado_columnas)
    
    # Imprimir la matriz con los números de fila y colores
    for indice, fila in enumerate(matriz):
        print(f"{indice} ", end="")
        for elemento in fila:
            if elemento == "#":
                print(Fore.RED + elemento + Style.RESET_ALL, end=" ")
            elif elemento == "I":
                print(Fore.GREEN + elemento + Style.RESET_ALL, end=" ")
            elif elemento == "F":
                print(Fore.BLUE + elemento + Style.RESET_ALL, end=" ")
            elif elemento == "*":
                print(Fore.YELLOW + elemento + Style.RESET_ALL, end=" ")
            else:
                print(elemento, end=" ")
        print()

def solicitar_obstaculos(matriz):
    while True:
        obstaculo = input("Ingrese la posición del obstáculo (fila,columna) o presione Enter para terminar: ")
        if obstaculo == "":
            break
        fila, columna = map(int, obstaculo.split(","))
        matriz[fila][columna] = "#"
        imprimir_matriz(matriz)
    return matriz

def solicitar_punto(mensaje, matriz, simbolo):
    while True:
        punto = input(f"Ingrese la posición del {mensaje} (fila,columna): ")
        fila, columna = map(int, punto.split(","))
        if matriz[fila][columna] == "[]":
            matriz[fila][columna] = simbolo
            imprimir_matriz(matriz)
            return fila, columna
        else:
            print("La posición está ocupada, elija otra.")

def heuristica(a, b):
    # Calcular la distancia euclidiana entre dos puntos
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def a_estrella(matriz, inicio, fin):
    tamano = len(matriz)
    # Movimientos en las ocho direcciones posibles (incluyendo diagonales)
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}
    f_score = {inicio: heuristica(inicio, fin)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == fin:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(inicio)  # Agregar el inicio al final del camino
            return path[::-1]
        
        for movimiento in movimientos:
            vecino = (current[0] + movimiento[0], current[1] + movimiento[1])
            if 0 <= vecino[0] < tamano and 0 <= vecino[1] < tamano:
                if matriz[vecino[0]][vecino[1]] == "#":
                    continue
                tent_g_score = g_score[current] + heuristica(current, vecino)
                
                if vecino not in g_score or tent_g_score < g_score[vecino]:
                    came_from[vecino] = current
                    g_score[vecino] = tent_g_score
                    f_score[vecino] = tent_g_score + heuristica(vecino, fin)
                    if vecino not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[vecino], vecino))
    
    return []

def main():
    # Solicitar al usuario que ingrese el tamaño de la matriz
    tamano = int(input("Ingrese el tamaño de la matriz: "))
    
    # Crear la matriz
    matriz = crear_matriz(tamano)
    imprimir_matriz(matriz)
    
    # Solicitar obstáculos
    matriz = solicitar_obstaculos(matriz)
    
    # Solicitar punto de inicio
    inicio = solicitar_punto("punto de inicio (I)", matriz, "I")
    
    # Solicitar punto final
    fin = solicitar_punto("punto final (F)", matriz, "F")
    
    # Buscar la ruta más corta con A*
    ruta = a_estrella(matriz, inicio, fin)
    
    if ruta:
        for paso in ruta:
            if matriz[paso[0]][paso[1]] == "[]":
                matriz[paso[0]][paso[1]] = "*"
        imprimir_matriz(matriz)
    else:
        print("No se encontró una ruta.")

if __name__ == "__main__":
    main()