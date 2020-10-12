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
cX = 0
cY = 0

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
    snap_bn = np.where(snap_b>155,d55,cero)
    snap_bn[snap_a > 210] = 0 # filtro en a para que la imagen no se contamine en condicion nocturna
    
    return snap_bn

def openf(compo):
    
    ee = np.ones((2,2),np.uint8)    #Elemento estructurante
    #transformacion open, se realiza primero erosion y luego dilatacion para eliminar ruido del en el entorno del objeto
    imagenProcesada = cv2.morphologyEx(compo, cv2.MORPH_OPEN, ee,iterations=5)  
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
    
    if count < 11000:  #Comprueba que el objeto sea visible, estableciendo un limite inferior para el area para los controles
        return (0,0,im)
    #solo toca la parte izquierda de la pantalla para indicar izquierda o derecha
    
    """Definición de las regiones de decision para el movimiento de la nave"""
    ml = im[:,250:445] #Region para moverse a la izquierda
    total_ml = ml.shape[0] * ml.shape[1] #dimension total de la region de decision para mov a izquierda
    count_ml = cv2.countNonZero(ml) # Area total ocupada por el objeto dentro de la region de decision
    
    mr = im[:,445:640] #Region para moverse a la derecha
    total_mr = mr.shape[0] * mr.shape[1]#dimension total de la region de decision para mov a derecha
    count_mr = cv2.countNonZero(mr)# Area total ocupada por el objeto dentro de la region de decision
    
    """Binarizacion de la imagen"""
    
    ret,thresh = cv2.threshold(im,127,255,0) #Se binariza la imagen para obtener los momentos con el fin de hallar el centroide
    
    """Calculo del contorno de la mano del jugador"""
    
    puntosContorno = encontrarContornos(thresh)
    areaContorno = cv2.contourArea(puntosContorno)
    imConContorno = cv2.drawContours(cv2.merge([im,im,im]), [puntosContorno], -1, (0,255,100), 3)
    
    
    hull = cv2.convexHull(puntosContorno) # Encuentra los Convexity deflects, cuyo contorno une los puntos ubicados en las esquinas del contorno en este caso los dedos
    imConContorno = cv2.drawContours(imConContorno, [hull], -1, (0,0,255), 3) # dibuja el contorno encontrado por convexHull
    areaConvexHull = cv2.contourArea(hull)
    
    """Calculo del area entre los dedos de la mano (espacios de deflexion de la concavidad) """
    
    areaEntreDedos = areaConvexHull-areaContorno
    
    if areaConvexHull != 0: 
        porcAreaEntreDedos = areaEntreDedos*100/areaConvexHull
    else:
        porcAreaEntreDedos = 0
        
        
    print("porAreaEntreDedos:  " , porcAreaEntreDedos)
    
    """Calulo del centroide de la imagen """
    
    M = cv2.moments(puntosContorno) # this function find the moments of the image, it returns a dictionary with the different moments calculated ¿
    
    if(M["m00"] != 0) :
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    coordenadasCentroide[0] = cX
    coordenadasCentroide[1] = cY
    
    print("Coordenadas Centroide: ",(cX,cY))

    
    

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
    """ Condicion para disparo, se el area entre los dedos de la mano es menor que 7000, significa que los dedos se contraen en forma de puño"""
    if porcentajeAreaObj >= 3 and porcentajeAreaObj <=10 and porcAreaEntreDedos <17: #Cuando hace puño con la mano, el porcentaje de area disminuye pero no es 0, se verifica que este en el rango
        maskDisparo = 3     #dispara
    else:
        maskDisparo = 0     #no dispara
    
    return (maskMov,maskDisparo,imConContorno)


def encontrarContornos(imagenBW):
    """Funcion que encuentra el contorno de la mano para el manejo de los controles del juego"""
    contornos,hierarchy = cv2.findContours(imagenBW,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = np.array([cv2.contourArea(i) for i in contornos])
    indiceMaxContour = np.argmax(areas) # El contorno con el area maxima se toma como el de la mano
    
    # print("numero de puntos de contorno: ",np.shape(contornos[indiceMaxContour]))
    return contornos[indiceMaxContour]
    



def loopImagen():
    
    HEIGHT = 480
    WIDTH = 640
    img = get_image()#Se obtiene un frame del video
    cb = componente_lab(img)
    cbd = openf(cb)
    #cv2.imshow("camara", img)#Se muestra la imagen capturada
    (controlMov,controlDisp,imagenContornos) = masks(cbd,screenSize=(WIDTH,HEIGHT))
    
    cv2.imshow("camara_bn", imagenContornos)#Se muestra la imagen prepocesada y segmentada en el espacio LAB junto con sus contornos
    
    
    return (controlMov,controlDisp)

   
def cerrarVideo():
    video.release()#Se cierra la camara
    cv2.destroyAllWindows()



    