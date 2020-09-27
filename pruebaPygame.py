# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 17:04:54 2020

@author: Jhon benavides
"""
#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initializing 
pygame.init()
 
#Setting up FPS 
FPS = 30
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
SPEED = 5
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
img_background = pygame.image.load("img_bg.jpg")

 
class Enemy(pygame.sprite.Sprite):
      def __init__(self,size):
        super().__init__() 
        #self.image = pygame.image.load("enemy.png")
        self.randomNumber = random.choice([10,20,30])
        self.size = (self.randomNumber,self.randomNumber)
        self.surf = pygame.Surface(self.size)
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))# me da info de las coordenadas de surf
        #Se genera un rectangulo a partir de la superficie centrado de forma aleatoria en la parte alta de la pantalla
      def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            #self.rect.top = 0 #vuelve y comienza a bajar desde arriba de la pantalla
            del self.surf #Libera memoria
            del self.rect
            self.randomNumber = random.choice([10,20,50])
            self.size = (self.randomNumber,self.randomNumber)
            self.surf = pygame.Surface(self.size)
            self.surf.fill(RED)
            self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40),0))# me da info de las coordenadas de surf
            
  
class Player(pygame.sprite.Sprite):   
    
    def __init__(self):
        super().__init__() 
        
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100))
        self.surf = pygame.image.load("nave_jugador.png")
        self.speed_p = 5
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed_p)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,self.speed_p)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-self.speed_p, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.speed_p, 0) 
                         
    def set_speed(self,speed):
         self.speed_p = speed
         
    def get_pos(self):
        return self.rect.midtop
    

         
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self,posInicial):
        super().__init__()
        self.surf = pygame.Surface((8, 8))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = posInicial)
        self.speed_bullet = 5
        self.lanzar = False
    def move(self):
         if self.lanzar == True:
             self.rect.move_ip(0,-3)
             if self.rect.bottom < 100:
                 self.kill()
    def set_lanzar(self):
        self.lanzar = True
    
             
             
         
#Setting up Sprites        
P1 = Player()
E1 = Enemy((10,10))
 
#Creating Sprites Groups
enemies = pygame.sprite.Group() #Genera el grupo para poder distiguir los enemigos

enemies.add(E1)#Al agregar un enemigo permite usar metodos de colision para saber si el jugador choca o no con los enemigos
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)#Se crea el grupo all_sprites para poder iterar en cada loop del juego sobre todos los elementos y poder dibujarlos
#con el uso de blit dibujarlos y moverlos segun el tipo de elemento
all_sprites.add(E1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
INC_ENEMYS = pygame.USEREVENT + 2
SHOOT = pygame.USEREVENT + 3
pygame.time.set_timer(INC_ENEMYS,5000)#Cada 10 segundos se aumenta el numero de enemigos por pantalla
pygame.time.set_timer(INC_SPEED, 5000) #se dispara el evento INC_SPEED cada que pasa un segundo
pygame.time.set_timer(SHOOT,2000)


P1.set_speed(10)
bullet = Bullet(P1.get_pos())
bullets_group = pygame.sprite.Group()

#Game Loop
while True:
    DISPLAYSURF.blit(img_background,(0,0)) # primer argumento es el objeto a dibujar y el segundo es la posicion
    #Cycles through all events occuring  
    #Observador de Eventos
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 1 #El evento aumenta la velocidad de los objetos que caen (los enemigos)
        if event.type == INC_ENEMYS:
            FramePerSec.tick(30)
            enemie = Enemy((10,10))
            enemies.add(enemie)
            all_sprites.add(enemie)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                bullet = Bullet(P1.get_pos())
                bullet.set_lanzar()
                bullets_group.add(bullet)
                all_sprites.add(bullet)
                
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.surf, entity.rect) # dibujar en la superficie la entity.surf con las coordenadas dadas por entity,.rect
        entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies): #verifica si el jugador choco con un enemigo
          DISPLAYSURF.fill(RED)
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()
          
    
    # detecta una colision entre la bala y un enemigo, de esta forma se aumenta el puntaje y se eliminan los elementos
    for bala,enemigos in pygame.sprite.groupcollide(bullets_group,enemies,False,False).items():
        for enemigo in enemigos:
            enemigo.kill()
            print("hubo un choque")
        bala.kill()
             
    pygame.display.update()
    FramePerSec.tick(FPS)
   
    
pygame.quit()
sys.exit()

