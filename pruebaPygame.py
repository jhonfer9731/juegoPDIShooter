# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 17:04:54 2020

@author: Christian Camilo Garzon, Jhon Fernando benavides
"""
#Imports
import pygame, sys
from pygame.locals import *
import random, time

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
 
"""Inicializacion de la pantalla del juego"""

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("ShooterGB") #Titulo del juego
img_background = pygame.image.load("img_bg.jpg")



 
class Enemy(pygame.sprite.Sprite):
    """ Descripcion: 
        
        Clase enemigo hereda de la clase Sprite, permite crear los enemigos del jugador, los cuales caeran 
        desde la parte superior en forma vertical y a medida que pase el tiempo incrementaran 
        su velocidad, al colisionar con el jugador este pierde una vida
        
        Se inicializa el objeto con un tamaño especificado de forma aleatoria
        
        Su posicion inicial se asigna de forma aleatoria 
        
        Cuando llega al final de la pantalla este se elimina y vuelve posicionarse desde la parte
        superior de la pantalla
    
    """
    def __init__(self,size):
        super().__init__() 
        #self.image = pygame.image.load("enemy.png")
        self.randomNumber = random.choice([10,20,30])
        self.size = (self.randomNumber,self.randomNumber) #Se genera su tamaño como un cuadrado de lado aleatorio
        self.surf = pygame.Surface(self.size)   #Se genera la superficie que aparecera la pantalla
        self.surf.fill(RED)
        self.speed = 5
        # La siguiente linea me da info de las coordenadas de surf
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))
        #Se genera un rectangulo a partir de la superficie centrado de forma aleatoria en la parte alta de la pantalla
    def move(self): 
        """Metodo que permite mover el enemigo, se ejecuta en el loop central del juego"""
        
        self.rect.move_ip(0,self.speed) # Funcion para mover el enemigo especificando la velocidad xy
      
        if (self.rect.top > SCREEN_HEIGHT): # Condicion cuando llega a la parte inferior y no colisiono con el jugador
            #self.rect.top = 0 #vuelve y comienza a bajar desde arriba de la pantalla
            del self.surf #Libera memoria
            del self.rect
            self.randomNumber = random.choice([10,20,50]) # Su tamaño se asigna nuevamente
            self.size = (self.randomNumber,self.randomNumber)  #Se genera su tamaño como un cuadrado de lado aleatorio
            self.surf = pygame.Surface(self.size) #Se genera la superficie que aparecera la pantalla
            self.surf.fill(RED)
            self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))# me da info de las coordenadas de surf
    def set_speed(self,speed):
        """ Metodo que permite establecer la velocidad del enemigo"""
        self.speed = speed
  
class Player(pygame.sprite.Sprite):   
    """ Descripcion: 
        
        Clase Player hereda de la clase Sprite, permite crear el jugador principal, el cual podra moverse
        en las 4 direcciones
        
        Se inicializa el objeto sin parametros al constructor
        
        Su posicion inicial se asigna en parte central inferior
        
        Este tendra la habilidad de moverse para esquivar a los enemigos y lanzar balas para eliminarlos
        
        Tiene una vida inicial asignada la cual disminuye al colisionar con un enemigo
    
    """
    
    def __init__(self):
        super().__init__() 
        
        self.surf = pygame.Surface((32, 32))#Se genera la superficie cuadrada que aparecera la pantalla
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)) #permite asignar las coordenadas del objeto y el centro de estas
        self.surf = pygame.image.load("nave_jugador.png") # Se cambia la superficie plana por una imagen
        self.speed_p = 5 # Se establece la magnitud de la velocidad incial
        
    def move(self): #Metodo que permite el movimiento del objeto cuando una tecla es presionada
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed_p)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,self.speed_p)
        if self.rect.left > 0: # Permite moverse a izq o der solo cuando el jugador este dentro del recuadro de la pantalla
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-self.speed_p, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.speed_p, 0) 
                         
    def set_speed(self,speed):
        """Metodo que permite cambiar la magnitud velocidad del jugador"""
        self.speed_p = speed
         
    def get_pos(self):
        """Metodo que entrega la posicion del jugador, centrada en la mitad superior del cuerpo de este"""
        return self.rect.midtop
    

         
class Bullet(pygame.sprite.Sprite):
    """
        Descripcion:
            
            Clase Bullet, permite instanciar una bala en el juego, la cual sera lanzada por el jugador
            
            Se inicializa con la posicion inicial la cual corresponde a la posicion actual del jugador
            
            Tiene un tamaño de 8x8  y una velocidad de 5 en direccion hacia arriba
    
    """
    
    def __init__(self,posInicial):
        """Constructor de la bala, inicializa el tamaño, las coordenadas, la velocidad y la activacion de lanzamiento"""
        super().__init__()
        self.surf = pygame.Surface((8, 8))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = posInicial)
        self.speed_bullet = 3
        self.lanzar = False
        
        
    def move(self):
        """Metodo que permite el movimiento de la bala en el juego"""
        if self.lanzar == True: # Permite el movimiento de la bala, solo ocurre cuando el jugador lo inique
            self.rect.move_ip(0,-self.speed_bullet)
            if self.rect.bottom < 100: # Permite eliminar el objeto cuando este alcanza una altura calculada con respecto a la dim de la pantalla
                self.kill()
                 
                 
    def set_lanzar(self):
        """funcion que activa el lanzamiento de la bala"""
        self.lanzar = True
    
             
             
"""Obejetos del juego """
 
#Se crean los objetos jugador y enemigos       
P1 = Player()
E1 = Enemy((10,10))
bullet = Bullet(P1.get_pos()) # Se crea el objeto bala y se inicializa en la posicion actual del jugador
 
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
pygame.time.set_timer(INC_ENEMYS,5000)#Cada 10 segundos se aumenta el numero de enemigos por pantalla, se dispara el evento
pygame.time.set_timer(INC_SPEED, 5000) #se dispara el evento INC_SPEED cada que pasa un segundo, se dispara el evento
pygame.time.set_timer(SHOOT,2000)


"""Loop principal del juego """


while True:
    
    DISPLAYSURF.blit(img_background,(0,0)) # Dibuja la imagen de fondo del juego
    
    
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
            
        if event.type == QUIT:#Evento disparado al cerrar la ventana del juego
            for entity in all_sprites:
                entity.kill() #Elimina todos los obejetos del juego y libera memoria
            pygame.quit() # Sale del juego
            sys.exit()
            
        if event.type == KEYUP: #Eventos de teclado
            if event.key == K_SPACE:
                bullet = Bullet(P1.get_pos())
                bullet.set_lanzar()
                bullets_group.add(bullet)
                all_sprites.add(bullet)
                
    #Mueve y re dibuja todos los objetos del juego
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.surf, entity.rect) # dibujar en la superficie el objeto (entity.surf) con las coordenadas dadas por entity,.rect
        entity.move() # Mueve los elementos del juego
 
    """Colisiones """
    
    """Jugador con Enemigos"""
    
    if pygame.sprite.spritecollideany(P1, enemies): #verifica si el jugador choco con algun enemigo
          DISPLAYSURF.fill(RED) #coloca la pantalla en rojo
          pygame.display.update() #Actualiza la pantalla del juego
          for entity in all_sprites:
                entity.kill()  #Elimina todos los elementos
          time.sleep(2)
          pygame.quit() # termina el juego
          sys.exit()
          
    """Balas con enemigos""" 
    
    # detecta una colision entre la bala y un enemigo, de esta forma se aumenta el puntaje y se eliminan los elementos
    for bala,enemigos in pygame.sprite.groupcollide(bullets_group,enemies,False,False).items():
        for enemigo in enemigos: # Si la bala choco alguno de los enemigos, los elimina
            enemigo.kill()
            print("hubo un choque")
        bala.kill() # Si la bala choco, elimina la bala
             
    pygame.display.update() # Actualiza la pantalla del juego
    FramePerSec.tick(FPS) # Genera un retardo para poder mostrar FPS cuadros por segundo
   
    
pygame.quit()
sys.exit()

