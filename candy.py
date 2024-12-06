import random

def generar_matriz(lista:list)->list:

    #genera matriz
    for i in range(len(lista)):

        for j in range(7):

            numero = random.randint(1,3)
            lista[i]["piezas"].append(numero)

    return lista

def validar_rango(numero: int, desde: int, hasta: int)->int:

    #valida dentro de un rango
    while numero < desde or numero > hasta:
        numero = int(input("Error, ingrese un numero valido: "))

    return numero

def verificar_posicion(lista: list, fila: int, columna: int) -> bool:
    resultado = False
    pos_usuario = lista[fila]["piezas"][columna]

    contador = 0

    #abajo
    for i in range(1, 3):  # Verifica las 2 posiciones siguientes hacia abajo
        if fila + i < len(lista) and lista[fila + i]["piezas"][columna] == pos_usuario:
            contador += 1
        else:
            break

    #arriba
    for i in range(1, 3):  # Verifica las 2 posiciones anteriores hacia arriba
        if fila - i >= 0 and lista[fila - i]["piezas"][columna] == pos_usuario:
            contador += 1
        else:
            break

    if contador >= 2:
        resultado = True

    return resultado

def mostrar_matriz(lista:list)->None:
    for i in range(len(lista)):

        print(lista[i]["piezas"])

def agregar_csv(puntos, nombre, puntuacion):
#agregar info al archivo
    archivo = open(puntos, 'a')
    texto = archivo.write(f"\nNombre: {nombre}\n Puntos: {puntuacion}\n")
    archivo.close()

def leer_csv(puntos):
#printear el contenido
    archivo = open(puntos, 'r+')
    for linea in archivo:
        print(linea, end="")
    archivo.close()

lista = [
{"piezas":[]},
{"piezas":[]},
{"piezas":[]},
{"piezas":[]}
]

lista = generar_matriz(lista)

mostrar_matriz(lista)

fila_ingreso = int(input("Elija una fila entre 0 y 3: "))

x = validar_rango(fila_ingreso, 0, 3)

columna_ingreso = int(input("Elija una columna entre 0 y 6: "))

y = validar_rango(columna_ingreso, 0, 6)

ganador = verificar_posicion(lista, x, y)

if ganador:
    print("Ha ganado 10 puntos")
    puntuacion = 10
else:
    print("Siga participando")
    puntuacion = 0

nombre = input("Ingrese su nombre de jugador: ")

agregar_csv("puntos.csv", nombre, puntuacion)
leer_csv("puntos.csv")
print("\nPuntuacion registrada correctamente\nFin del juego.")