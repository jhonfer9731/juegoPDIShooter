# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 08:31:46 2020

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:46:19 2020

@author: Camiilo
"""

from cv2 import *
import numpy as np
import time
import sys

camara = 0   #Defecto es 0
video = cv2.VideoCapture(camara) #Se inicia la captura de video


def get_image():
     # leer la captura
     retval, im = video.read()#Se inica la lectura del video
     return im
 
def normi(compo):
    compo = compo.astype(np.float64)
    compo = compo/np.max(compo)
    compo = 255 * compo 
    compo = compo.astype('uint8')
    return compo    
    
def componente_lab(snap):
    cero = np.uint8(0)
    d55 = np.uint8(255)
    snap_lab = cvtColor(snap, COLOR_BGR2LAB)    # Se cambia de espacio de color de RGB para LAB usando funcion de cv2
    snap_b = snap_lab[:,:,2]                          # Se obtiene componente b de la imagen
    snap_bn = normi(snap_b)
    snap_bn = np.where(snap_b>160,d55,cero)

    return snap_bn

def openf(compo):
    ee = np.ones((3,3),np.uint8)    #Elemento estructurante

    # Ciclo para la erosion
    for i in range(1, 5):
        compo = cv2.erode(compo, ee, iterations = i)
        #cv2.imshow('Imagen Erosionada', compo)
        #cv2.waitKey(500)
        
    for i in range(1, 10):
        compo = cv2.dilate(compo, ee, iterations = i)
        #cv2.imshow('Imagen Dilatada ', a)
        #cv2.waitKey(500)
    
    return  compo

def masks(im):

    mask = 0
    ml = im[240:480 , 0:213]
    total_ml = ml.shape[0] * ml.shape[1]
    count_ml = cv2.countNonZero(ml)
    
    mr = im[240:480 , 427:640]
    total_mr = mr.shape[0] * mr.shape[1]
    count_mr = cv2.countNonZero(mr)
    
    mu = im[0:240 , 213:427]
    total_mu = mu.shape[0] * mu.shape[1]
    count_mu = cv2.countNonZero(mu)
    
    md = im[240:480 , 213:427]
    total_md = md.shape[0] * md.shape[1]
    count_md = cv2.countNonZero(md)
    
    if (count_ml/total_ml)*100 >= 20:
        mask = 1
    elif (count_mr/total_mr)*100 >= 20:
        mask = 2
    elif (count_mu/total_mu)*100 >= 20:
        mask = 3
    elif (count_md/total_md)*100 >= 20:
        mask = 4 
    
    return mask




def loopImagen():
    img = get_image()#Se obtiene un frame del video    OJOOOOOOOOOO
    cb = componente_lab(img)
    cbd = openf(cb)
    #cv2.imshow("camara", img)#Se muestra la imagen capturada
    cv2.imshow("camara_bn", cbd)#Se muestra la componente b normalizada de LAB de la imagen capturada
    here = masks(cbd)
    if here != 0:
        print (here)
    

   
def cerrarVideo():
    video.release()#Se cierra la camara
    cv2.destroyAllWindows()



    