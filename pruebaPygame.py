# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 17:04:54 2020

@author: Christian Camilo Garzon, Jhon Fernando benavides
"""
#Imports

from cv2 import *
import numpy as np
from elementosJuego import *
from game_pdiv2 import *


if not video:
    sys.exit(1)
#Inicializacion del juego
pygame.init()
 
#Setting up FPS 
FPS = 30 #Cuadros por segundo a los que va a correr el juego
FramePerSec = pygame.time.Clock() #Reloj que permite la sincronizacion del juego
 
"""Colores principales"""
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

"""Variables para uso en el programa"""

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
SPEED = 5
VIDAS_INCIALES = 50
BALAS_INICIALES = 15

 
"""Inicializacion de la pantalla del juego"""

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("ShooterGB") #Titulo del juego
img_background = pygame.image.load("img_bg.jpg")

                          
"""Obejetos del juego """
 
#Se crean los objetos jugador y enemigos       
P1 = Player(VIDAS_INCIALES)
E1 = Enemy((10,10))
bullet = Bullet(P1.get_pos()) # Se crea el objeto bala y se inicializa en la posicion actual del jugador
marcador = marcadorVidas(ancho = 200) # Inicializacion del marcador con el ancho de la barra en pixeles
marcador.modificarMarcador(VIDAS_INCIALES,VIDAS_INCIALES) # Se asigna el valor maximo de vidas y el numero actual que al principio es el maximo tambien
marcador2 = MarcadorMunicion(ancho = 200)
marcador2.modificarMarcador(BALAS_INICIALES,BALAS_INICIALES)

PUNTAJE_JUGADOR = P1.get_puntaje()

"""Textos"""

font = pygame.font.SysFont('comic sans ms', 16)
textoVidas = font.render('Vida disponible', True, WHITE, BLACK)
coorTextoVidas = textoVidas.get_rect(center=(200,30))
textoBalas = font.render('Balas disponibles', True, WHITE, BLACK)
coorTextoBalas = textoBalas.get_rect(center=(200,80))

font = pygame.font.SysFont('comic sans ms', 24)
textoPuntaje = font.render('Puntaje: '+str(PUNTAJE_JUGADOR), True, WHITE, BLACK)
coorTextoPuntaje = textoBalas.get_rect(center=(SCREEN_WIDTH-100,5))
"""Creacion de grupos"""

bullets_group = pygame.sprite.Group() #Se crea el grupo donde estaran todas las balas activas

enemies = pygame.sprite.Group() #Genera el grupo conformado unicamente por los enemigos
enemies.add(E1)#Al agregar un enemigo permite usar metodos de colision para saber si el jugador choca o no con los enemigos

all_sprites = pygame.sprite.Group() #Se crea el grupo all_sprites para poder iterar en cada loop del juego sobre todos los elementos y poder dibujarlos
all_sprites.add(P1) # Se agrega el jugador al grupo
all_sprites.add(E1) # Se agrega el enemigo al grupo

"""Eventos"""
 
#Se agregan eventos que van a ejecutarse cada vez que pase un intervalo de tiempo
#el cual esta dado por pygame.time.set_timer
INC_SPEED = pygame.USEREVENT + 1
INC_ENEMYS = pygame.USEREVENT + 2
SHOOT = pygame.USEREVENT + 3
RECARGA_BALAS = pygame.USEREVENT + 4
pygame.time.set_timer(INC_ENEMYS,5000)#Cada 10 segundos se aumenta el numero de enemigos por pantalla, se dispara el evento
pygame.time.set_timer(INC_SPEED, 5000) #se dispara el evento INC_SPEED cada que pasa un segundo, se dispara el evento
pygame.time.set_timer(SHOOT,2000)



"""Timer balas"""

banderaRecarga = True

"""Loop principal del juego """



while True:
    
    DISPLAYSURF.blit(img_background,(0,0)) # Dibuja la imagen de fondo del juego
    
    if P1.get_numMuniciones() == 0 and banderaRecarga:
        print("Entro aqui get_numMuniciones == 0")
        pygame.time.set_timer(RECARGA_BALAS,4000) # Dispara el evento para realizar la recarga de las balas despues de 4 segundos   
        banderaRecarga = False
        
    ubicacionControl,balaControl = loopImagen()
    # print(ubicacionControl)
    
    if ubicacionControl == 1: #izquierda
        P1.set_speed(5)
    elif ubicacionControl == 2: #Derecha
        P1.set_speed(-5)
    else:
        P1.set_speed(0)
        
    if balaControl == 3 and P1.get_numMuniciones() > 0: #Eventos de teclado
    
        if tiempoDespuesDisparo == 0:
            bullet = Bullet(P1.get_pos())
            bullet.set_lanzar()
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            P1.disminuirMuniciones() #Se disminuyen las balas disponibles
            marcador2.modificarMarcador(BALAS_INICIALES,P1.get_numMuniciones())
            print("Municiones Disp:", P1.get_numMuniciones())
            tiempoDespuesDisparo += 1
            
        elif tiempoDespuesDisparo == 12:
            tiempoDespuesDisparo = 0
        else:
            tiempoDespuesDisparo += 1 
    else:
        tiempoDespuesDisparo = 0
        
    # elif ubicacionControl == 4 : #abajo
    
    # elif ubicacionControl == 3 : #arriba
    """Observador de Eventos"""
    
    for event in pygame.event.get(): #En cada ciclo, se verifica si se dispararon algunos eventos
        
        if event.type == INC_SPEED: #Evento disparado por timer para incrementar velocidad enemigos
            SPEED += 1
            for enemy in enemies:
                enemy.set_speed(SPEED)
            
        if event.type == INC_ENEMYS:#Evento disparado por timer para incrementar el numero de enemigos
            #FramePerSec.tick(30)
            enemie = Enemy((10,10))#Se crea un enemigo nuevo
            enemies.add(enemie)#Se agrega a sus grupos
            all_sprites.add(enemie)
            
        if event.type == RECARGA_BALAS:
            print("Recargo balas")
            P1.set_Municiones(15)
            pygame.time.set_timer(RECARGA_BALAS,0) # Deshabilita el timer para el evento
            banderaRecarga = True
            DISPLAYSURF.blit(marcador2.surf,marcador2.rect)
        if event.type == QUIT:#Evento disparado al cerrar la ventana del juego
            for entity in all_sprites:
                entity.kill() #Elimina todos los obejetos del juego y libera memoria
            cerrarVideo()
            pygame.quit() # Sale del juego
            sys.exit()
        
                
    """Mueve y re dibuja todos los objetos del juego"""
    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.surf, entity.rect) # dibujar en la superficie el objeto (entity.surf) con las coordenadas dadas por entity,.rect
        entity.move() # Mueve los elementos del juego
    
    
    """Colisiones """
    
    """Jugador con Enemigos"""
    
    if pygame.sprite.spritecollideany(P1, enemies): #verifica si el jugador choco con algun enemigo
        print("vidas" ,P1.get_NumeroVidas())
        if P1.get_NumeroVidas() <= 0: #Si el jugador consumio sus vidas, termina el juego
            DISPLAYSURF.fill(RED) #coloca la pantalla en rojo  
            font = pygame.font.SysFont('comic sans ms', 60)
            textoPuntaje = font.render('Puntaje final: '+str(PUNTAJE_JUGADOR), True, WHITE)
            coorTextoPuntaje = textoBalas.get_rect(center=(SCREEN_WIDTH//3,SCREEN_HEIGHT//2))
            DISPLAYSURF.blit(textoPuntaje,coorTextoPuntaje)
            del marcador
            del marcador2
            pygame.display.update() #Actualiza la pantalla del juego
            for entity in all_sprites:
                  entity.kill()  #Elimina todos los elementos
            time.sleep(2)
            cerrarVideo()
            pygame.quit() # termina el juego
            sys.exit()
        else:   # Si tiene vidas, disminuya y muestra en el marcador
            P1.disminuir_vidas(1)
            marcador.modificarMarcador(VIDAS_INCIALES,P1.get_NumeroVidas())
            
    """Balas con enemigos""" 
    
    # detecta una colision entre la bala y un enemigo, de esta forma se aumenta el puntaje y se eliminan los elementos
    for bala,enemigos in pygame.sprite.groupcollide(bullets_group,enemies,False,False).items():
        for enemigo in enemigos: # Si la bala choco alguno de los enemigos, los elimina
            enemigo.kill()
            P1.incrementarPuntaje(4) # si la bala elimina al enemigo aumenta el puntaje de jugador
            PUNTAJE_JUGADOR = P1.get_puntaje()
            textoPuntaje = font.render('Puntaje: '+str(PUNTAJE_JUGADOR), True, WHITE, BLACK)
            print("hubo un choque")
        bala.kill() # Si la bala choco, elimina la bala


    DISPLAYSURF.blit(textoPuntaje,coorTextoPuntaje)
    DISPLAYSURF.blit(textoBalas,coorTextoBalas)
    DISPLAYSURF.blit(textoVidas,coorTextoVidas)
    DISPLAYSURF.blit(marcador.surf,marcador.rect)
    DISPLAYSURF.blit(marcador2.surf,marcador2.rect)
    
    pygame.display.update() # Actualiza la pantalla del juego
    FramePerSec.tick(FPS) # Genera un retardo para poder mostrar FPS cuadros por segundo
    
    
pygame.quit()
sys.exit()

