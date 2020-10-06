# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 20:04:00 2020

@author: user
"""

import pygame, sys
from pygame.locals import *
import random, time

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
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
        self.imagen = pygame.image.load("meteoro.png")
        self.imagen2 = pygame.image.load("misil.png")
        self.imagen3 = pygame.image.load("bomba-nuclear.png")
        self.randomNumber = random.choice([128,64,32])
        self.size = (self.randomNumber,self.randomNumber) #Se genera su tamaño como un cuadrado de lado aleatorio
        self.surf = pygame.Surface(self.size)   #Se genera la superficie que aparecera la pantalla
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))
        if(self.randomNumber == 32):
            self.surf = self.imagen
        elif(self.randomNumber ==64):
            self.surf = self.imagen2
        elif self.randomNumber ==128 :
            self.surf = self.imagen3
        self.speed = 5
        # La siguiente linea me da info de las coordenadas de surf
        
        #Se genera un rectangulo a partir de la superficie centrado de forma aleatoria en la parte alta de la pantalla
    def move(self): 
        """Metodo que permite mover el enemigo, se ejecuta en el loop central del juego"""
        
        self.rect.move_ip(0,self.speed) # Funcion para mover el enemigo especificando la velocidad xy
      
        if (self.rect.top > SCREEN_HEIGHT): # Condicion cuando llega a la parte inferior y no colisiono con el jugador
            #self.rect.top = 0 #vuelve y comienza a bajar desde arriba de la pantalla
            del self.surf #Libera memoria
            del self.rect
            self.randomNumber = random.choice([128,64,32]) # Su tamaño se asigna nuevamente
            self.size = (self.randomNumber,self.randomNumber)  #Se genera su tamaño como un cuadrado de lado aleatorio
            self.surf = pygame.Surface(self.size) #Se genera la superficie que aparecera la pantalla
            self.surf.fill(RED)
            self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))# me da info de las coordenadas de surf
            if(self.randomNumber == 32):
                self.surf = self.imagen
            elif(self.randomNumber ==64):
                self.surf = self.imagen2
            elif self.randomNumber ==128 :
                self.surf = self.imagen3
                
                
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
        self.surf = pygame.image.load("bala.png")
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
    