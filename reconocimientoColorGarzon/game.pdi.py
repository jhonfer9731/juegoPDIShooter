# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:46:19 2020

@author: Camiilo
"""

from cv2 import *
import numpy as np
import time
import sys

def get_image():
     # leer la captura
     retval, im = video.read()#Se inica la lectura del video
     return im
 
def componente_b(snap):
    
    cero = np.uint8(0)
    d55 = np.uint8(255)
    
    snap_lab = cvtColor(snap, COLOR_BGR2LAB)    # Se cambia de espacio de color de RGB para LAB usando funcion de cv2
    
    snap_b = snap_lab[:,:,2]                          # Se obtiene componente b de la imagen
    snap_b= np.where(snap_b<=165,cero,snap_b)  # Se llevan a cero los valores que esten por debajo del filtro

    snap_a = snap_lab[:,:,1]
    snap_a = np.where(snap_a<=95,cero,snap_a)
    
    snap_L = snap_lab[:,:,0]                          # Se obtiene componente b de la imagen
    snap_L = snap_L.astype(np.float64)                    # Se convierte la imagen entrante en doble para poder operarla
    snap_Ln = snap_L/np.max(snap_L)             # Se normalizan las intensidades de la imagen
    snap_Ln = 255 * snap_Ln
    snap_Ln = snap_Ln.astype('uint8') 
    snap_L = np.where(snap_Ln<=135,cero,snap_L)
    
    snap_lab[snap_a == 0] = 0
    snap_lab[snap_L == 0] = 0
    snap_lab[snap_b == 0] = 0
    
   
    snap[snap_lab == 0] = 0
    
    

    return snap_lab



if __name__=='__main__':
    
    camara = 0   #Defecto es 0
    video = cv2.VideoCapture(camara) #Se inicia la captura de video
    if not video:
        sys.exit(1)
     
    while True: 
        img = get_image()#Se obtiene un frame del video    OJOOOOOOOOOO
        if img is None:
            break
        cb = componente_b(img)
        cv2.imshow("camara_norm", img)#Se muestra la imagen capturada
        cv2.imshow("camara_b", cb)#Se muestra la componente b de LAB de la imagen capturada
        
        if cv2.waitKey(34) == 27:#Espera por 'ESC'
            break
    video.release()#Se cierra la camara
    cv2.destroyAllWindows()



    
    
    
    
    
    