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
coordenadasCentroide = [0,0]

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
    snap_b = snap_lab[:,:,2] 
    snap_a = snap_lab[:,:,1]                         # Se obtiene componente b de la imagen
    snap_bn = np.where(snap_b>170,d55,cero)
    snap_bn[snap_a > 157] = 0 # filtro en a para que la imagen no se contamine en condicion nocturna
    
    return snap_bn

def openf(compo):
    
    ee = np.ones((2,2),np.uint8)    #Elemento estructurante
    #transformacion open, se realiza primero erosion y luego dilatacion
    imagenProcesada = cv2.morphologyEx(compo, cv2.MORPH_OPEN, ee,iterations=6)  
    imagenProcesada = cv2.dilate(compo,ee,iterations = 3)
    # Ciclo para la erosion
    # for i in range(1, 30):
    #     compo = cv2.erode(compo, ee, iterations = i)
    # for i in range(1, 15):
    #     compo = cv2.dilate(compo, ee, iterations = i)
    return  imagenProcesada

def masks(im,screenSize):
    #the shape of the image is (height,width)
    width = screenSize[0]
    height = screenSize[1]
    #mask = [0,0] # control de movimiento y disparo
    total = im.shape[0] * im.shape[1] # numero de pixeles de la imagen original de un canal
    count = cv2.countNonZero(im)# numero de pixeles del objeto en la imagen original
    
    if count < 13000:
        return (0,0)
    #solo toca la parte izquierda de la pantalla para indicar izquierda o derecha
    
    """Definición de las regiones de decision para el movimiento de la nave"""
    ml = im[:,250:445] #Region para moverse a la izquierda
    total_ml = ml.shape[0] * ml.shape[1] #dimension total de la region de decision para mov a izquierda
    count_ml = cv2.countNonZero(ml) # Area total ocupada por el objeto dentro de la region de decision
    
    mr = im[:,445:640] #Region para moverse a la derecha
    total_mr = mr.shape[0] * mr.shape[1]#dimension total de la region de decision para mov a derecha
    count_mr = cv2.countNonZero(mr)# Area total ocupada por el objeto dentro de la region de decision
    
    
    """Calulo del centroide de la imagen """
    ret,thresh = cv2.threshold(im,127,255,0) #Se binariza la imagen para obtener los momentos con el fin de hallar el centroide
    M = cv2.moments(thresh) # this function find the moments of the image, it returns a dictionary with the different moments calculated ¿
    
    if(M["m00"] != 0) :
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    coordenadasCentroide[0] = cX
    coordenadasCentroide[1] = cY
    
    #print("area para bala:",(count/total)*100 )

    """ Condiciones que permiten activar el movimiento a derecha e izquierda al igual que el disparo"""
    
    if (count_ml/total_ml)*100 >= 10:   # Si el procentaje del area ocupada por el objeto con respecto a la region de decision es mayor del 10% 
        if coordenadasCentroide[0] < 430 and coordenadasCentroide[0] > 250: #se pregunta si el centroide del objeto esta en el rango especificado
            maskMov = 1 # Se mueve a la izquierda
        else:
            maskMov = 0 #Si no esta en el rango no se mueve
    elif (count_mr/total_mr)*100 >= 10: # Se repite el mismo proceso anterior pero esta vez para la region de decision a derecha
        if coordenadasCentroide[0] < 640 and coordenadasCentroide[0] > 460:
            maskMov = 2  # Se mueve a la derecha
        else:
            maskMov = 0 #Si no esta en el rango no se mueve
    else:
        maskMov = 0 #Si el porcentaje de area ocupada del objeto no es el suficiente no se mueve
        
    porcentajeAreaObj = (count/total)*100 #se verifica el porcentaje de area ocupada por el objeto respecto a la pantalla original
    if porcentajeAreaObj >= 3 and porcentajeAreaObj <=8: #Cuando hace puño con la mano, el porcentaje de area disminuye, se verifica que este en el rango
        maskDisparo = 3     #dispara
    else:
        maskDisparo = 0     #no dispara
    
    return (maskMov,maskDisparo)




def loopImagen():
    
    HEIGHT = 480
    WIDTH = 640
    img = get_image()#Se obtiene un frame del video
    cb = componente_lab(img)
    cbd = openf(cb)
    #cv2.imshow("camara", img)#Se muestra la imagen capturada
    cv2.imshow("camara_bn", cbd)#Se muestra la componente b normalizada de LAB de la imagen capturada
    
    controlMov,controlDisp = masks(cbd,screenSize=(WIDTH,HEIGHT))
    return (controlMov,controlDisp)

   
def cerrarVideo():
    video.release()#Se cierra la camara
    cv2.destroyAllWindows()



    