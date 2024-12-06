import pygame
from colores import *
from candy import *
pygame.init()

ANCHO_VENTANA = 1000
ALTO_VENTANA = 500
COLOR_NARANJA = (220, 80, 10)

#imagenes y rect
imagen_play = pygame.image.load("boton2.jpg")
imagen_play = pygame.transform.scale(imagen_play,(150,150))
candy_logo = pygame.image.load("candycrushlogo.png")
candy_logo = pygame.transform.scale(candy_logo,(560,250))
rect_play = pygame.Rect(400,320,150,150)
caramelo_rojo  = pygame.image.load("caramelorojo.png")
caramelo_rojo = pygame.transform.scale(caramelo_rojo,(100,100))
caramelo_azul  = pygame.image.load("carameloazul.png")
caramelo_azul = pygame.transform.scale(caramelo_azul,(100,100))
caramelo_amarillo  = pygame.image.load("carameloamarillo.png")
caramelo_amarillo = pygame.transform.scale(caramelo_amarillo,(100,100))
tablero = pygame.Rect(30, 30, 730, 450)
ingreso_nombre_rect = pygame.Rect(320,300,350,80)
puntos_rect = pygame.Rect(20, 30, 730, 450)


#fuentes
font_input = pygame.font.SysFont("Arial", 60)
ingreso = ""
fuente = pygame.font.SysFont("Arial", 60)
fuente2 = pygame.font.SysFont("Arial", 150)
fuente3 = pygame.font.SysFont("Arial", 50)
fuente4 = pygame.font.SysFont("Arial", 20)

#musica
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("Crash_soundtrack.mp3")
volumen = 0.03
sonido_fondo.set_volume(volumen)

#inicio la pantalla con sus margenes
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

#Seteo un título en la pantalla
pygame.display.set_caption("CandyCrushUTN")

#variables
segundos = "10"
puntos = "0"
inicio = "3"
tiempo = "TIEMPO"
puntaje = "PUNTOS"
name = "INGRESE SU NICKNAME"
score = "SCOREBOARD"

#defino timer
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos,1000)
pygame.time.set_timer(timer_segundos,1200)


#flags
flag_correr = True
flag_mostrar = True
flag_mostrar_logo = True
flag_tablero_fondo = False
fin_juego = False
flag_ingreso = False
fin_tiempo = False
fin_tiempo_inicio = False

def imprimir_caramelos(lista: list, pantalla, caramelo_rojo, caramelo_azul, caramelo_amarillo): #imprimir caramelos
    coordenadas_fila = 40 # primera fila
    for objeto in lista:
        coordenadas_columna = 50 # primera columna
        for caramelo in objeto["piezas"]:
            if caramelo == 1: 
                pantalla.blit(caramelo_rojo,(coordenadas_columna, coordenadas_fila))
            elif caramelo == 2:
                pantalla.blit(caramelo_azul,(coordenadas_columna, coordenadas_fila))
            elif caramelo == 3:
                pantalla.blit(caramelo_amarillo,(coordenadas_columna, coordenadas_fila))
            coordenadas_columna += 100
            if coordenadas_columna >= 700:
                coordenadas_columna = 100
        if coordenadas_fila >= 400:
            coordenadas_fila = 150
        coordenadas_fila += 110 

while flag_correr:
    sonido_fondo.play()
    #guardo los eventos de la ventada en una lista
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        #Si el tipo de evento es salir (detecta si el usuario cierra la ventana)
        if evento.type == pygame.QUIT:
            flag_correr = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_play.collidepoint(evento.pos): #si el click esta dentro de la imagen play arranca el juego principal
                flag_mostrar = False
                flag_mostrar_logo = False
                flag_tablero_fondo = True
            if tablero.collidepoint(evento.pos):
                coordenada_y = int(round(evento.pos[0] / 100,0)-1)
                coordenada_x = int(round((evento.pos[1]-100) / 100,0))
                intento_juego = verificar_posicion(lista, coordenada_x,coordenada_y)
                if intento_juego == True and fin_tiempo_inicio: #si gana
                    lista = [
                        {"piezas":[]},
                        {"piezas":[]},
                        {"piezas":[]},
                        {"piezas":[]}
                        ]
                    generar_matriz(lista) #genero otra matriz
                    puntos = int(puntos) + 10 # sumo puntos
                    pygame.display.flip()
                elif intento_juego == False and fin_tiempo_inicio: # si falla
                    lista = [
                        {"piezas":[]},
                        {"piezas":[]},
                        {"piezas":[]},
                        {"piezas":[]}
                        ]
                    generar_matriz(lista) #genero otra matriz
                    segundos = int(segundos) -1 # resta un segundo
                    puntos = int(puntos) -1 # resta un punto
                    pygame.display.flip()
        if evento.type == pygame.USEREVENT:
            if evento.type == timer_segundos:
                if fin_tiempo_inicio == False and flag_tablero_fondo:
                    inicio = int(inicio) - 1
                    if int(inicio) == 0:
                        fin_tiempo_inicio = True
                if fin_tiempo == False and fin_tiempo_inicio:
                    segundos = int(segundos) -1
                    if segundos <= 0: # si segundos es menor o igual a 0
                        fin_tiempo = True
                        segundos = "Tiempo"
                        fin_juego = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE: # si el usuario quiere borrar un caracter
                ingreso = ingreso[0:-1]
            elif evento.key == pygame.K_RETURN:  # detecta el enter
                flag_ingreso = True
                agregar_csv("puntos.csv", ingreso, puntos)
                leer_csv("puntos.csv") #printea el contenido de csv
            else:
                ingreso += evento.unicode

    #pongo un fondo de color
    pantalla.fill(COLOR_NARANJA)
    
    #se van mostrando las imagenes y demas
    if fin_juego == False:
        if flag_mostrar:
            pygame.draw.rect(pantalla,COLOR_AMARILLO,rect_play)
            pantalla.blit(imagen_play,(400,320))
        if flag_mostrar_logo:
            pantalla.blit(candy_logo,(200,50))
        if flag_tablero_fondo:
            pygame.draw.rect(pantalla, GRAY37, tablero)
            if fin_tiempo_inicio == False:
                inicio_tiempo = fuente2.render(str(inicio), True, RED1 )
                pantalla.blit(inicio_tiempo, (350,150))
            else:
                segundos_texto = fuente.render(str(segundos), True, COLOR_BLANCO )
                pantalla.blit(segundos_texto, (800, 100))
                seg = fuente3.render(tiempo, True, CORNFLOWERBLUE)
                pantalla.blit(seg, (770,20))
                texto = fuente.render(str(puntos), True, COLOR_BLANCO)
                pantalla.blit(texto,(800, 300))
                pts = fuente3.render(puntaje, True, CORNFLOWERBLUE)
                pantalla.blit(pts, (770, 220))
                imprimir_caramelos(lista,pantalla, caramelo_rojo,caramelo_azul,caramelo_amarillo)
    elif fin_juego and flag_ingreso == False:
        texto_name = fuente3.render(name, True, COLOR_BLANCO )
        pantalla.blit(texto_name, (200,200))
        pygame.draw.rect(pantalla, ALICEBLUE, ingreso_nombre_rect , 2)
        font_input_surface = font_input.render(ingreso, True, BLACK) 
        pantalla.blit(font_input_surface, ( ingreso_nombre_rect.x+5 , ingreso_nombre_rect.y + 5 ))

    if flag_ingreso:
        pygame.draw.rect(pantalla, GRAY37, puntos_rect)
        tabla_puntaje = fuente3.render(score, True, RED1 )
        pantalla.blit(tabla_puntaje, (18,25))
        archivo = open("puntos.csv", 'r+')
        cord_fila = 30
        cord_columna = 60
        for linea in archivo:
            cord_columna += 20
            if cord_columna > 450:
                cord_columna = 90
                cord_fila += 140
            txt = fuente4.render(linea, True, COLOR_BLANCO)
            pantalla.blit(txt, (cord_fila, cord_columna))
        archivo.close()


    pygame.display.flip()
sonido_fondo.stop()
pygame.quit()  