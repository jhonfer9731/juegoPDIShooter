# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 20:10:16 2020

@author: user
"""

import cv2
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import copy

    
    
def stackToImg(im1,im2): # Permite concatenar 2 imagenes verticalmente
    scale_percent = 60
    #calculate the 50 percent of original dimensions
    width = int(im1.shape[1] * scale_percent / 100)
    height = int(im1.shape[0] * scale_percent / 100)
    im1New = cv2.resize(im1,(width,height))
    im2New = cv2.resize(im2,(width,height))
    im2Channels = np.vstack((im1New,im2New))
    return im2Channels


def preprocesar_img(imagen):
    """Se encarga de aplicar los filtros adecuados y escojer el espacio de color adecuado para la deteccion del control"""
    imagenProcesada = copy.deepcopy(imagen)
    #hist_curve_alt(imagenProcesada)
    cero = np.uint8(0)
    d55 = np.uint8(255)
    snap_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)    # Se cambia de espacio de color de RGB para LAB usando funcion de cv2

    snap_b = snap_lab[:,:,2]                          # Se obtiene componente b de la imagen
    snap_b= np.where(snap_b<=165,cero,snap_b)  # Se llevan a cero los valores que esten por debajo del filtro

    snap_a = snap_lab[:,:,1]
    snap_a = np.where(snap_a<=95,cero,snap_a)
   
    snap_L = snap_lab[:,:,0]                          # Se obtiene componente b de la imagen
    snap_L = snap_L.astype(np.float64)                    # Se convierte la imagen entrante en doble para poder operarla
    snap_Ln = snap_L/np.max(snap_L)             # Se normalizan las intensidades de la imagen
    snap_Ln = 255 * snap_Ln
    snap_Ln = snap_Ln.astype('uint8') 
    snap_L = np.where(snap_Ln<=125,cero,snap_L)
    
    snap_lab[snap_a == 0] = 0
    snap_lab[snap_L == 0] = 0
    snap_lab[snap_b == 0] = 0
    
   
    imagenProcesada[snap_lab == 0] = 0
    
    
    """Operaciones morfologicas"""
    #ventanaDeslizante = np.ones((8,8),np.uint8)
    #imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_OPEN, ventanaDeslizante)  #transformacion open, se realiza primero erosion y luego dilatacion

    #imagenProcesada = cv2.erode(imagenProcesada,ventanaDeslizante);
    #Se eliminina los huecos negros producidos por las letras del marcador
    ventanaDeslizante = np.ones((12,12),np.uint8)
    imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_CLOSE, ventanaDeslizante)  #transformacion open, se realiza primero erosion y luego dilatacion
    
    #imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_OPEN, ventanaDeslizante)
    #ventanaDeslizante = np.ones((12,12),np.uint8)
    #imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_CLOSE, ventanaDeslizante) 
    
    
    imagen[imagenProcesada == 0] = 0
    
    
    """Center of mass (centroide)"""
    # convert image to grayscale image
    gray_image = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    ret,markers = cv2.connectedComponents(gray_image)
    cmap = plt.cm.get_cmap("jet")
    area = np.zeros(ret)
    for i in range(1,ret):
        area[i] = np.sum(markers==i)
    mayorArea = np.argmax(area)
    if mayorArea == 0:
        mayorArea = 1

    markers = np.where(markers == mayorArea,d55,cero)
    gray_image[markers == 0] = 0
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    
    # calculate moments of binary image
    M = cv2.moments(thresh)
    
    # calculate x,y coordinate of center
    if(M["m00"] != 0) :
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print((cX,cY))
    
    
    """ Deteccion de bordes del marcador"""
    # ret,imBW = cv2.threshold(imagenProcesada,100,255,cv2.THRESH_BINARY)
    # fil,col = np.where(imBW[:,:,0])
    # imBW[:,:,:] = 0
    # if fil.size > 40 and col.size > 40:
    #     limites = [np.min(fil),np.max(fil),np.min(col),np.max(col)]
        
    #     if limites[0] > 0 and limites[0] < 720 and limites[1] > 0 and limites[1] < 720 and limites[2] > 0 and limites[2] < 1280 and limites[3] > 0 and limites[3] < 1280 :
    #         imBW[limites[0]:limites[1],limites[2]:limites[3],:] = 250
        
    #imagenGray3Ch = cv2.merge((imBW,imBW,imBW)) #Permite juntar las 3 capas en una imagen de 3 canales
    #imagenesFila = stackToImg(imagen,imBW) #junta 2 imagenes en la misma fila
    
    
    return markers
    
    
def hist_curve_alt(im):
    #bins = np.arange(256).reshape(256,1)
    if len(im.shape) == 2:
        color = ['k']
    else:
        color = ['-b','-g','-r']
    fig = plt.figure()
    #hist_item = cv2.calcHist([im[:,:,0]],[0],None,[100],[0,100])
    #plt.plot(np.arange(0,100),hist_item,'-b');
    hist_item = cv2.calcHist([im[:,:,1]],[0],None,[382],[-127,255])
    plt.plot(np.arange(-127,255),hist_item,'-g');
    hist_item = cv2.calcHist([im[:,:,2]],[0],None,[382],[-127,255])
    plt.plot(np.arange(-127,255),hist_item,'-r');
   # for ch,col in enumerate(color):
        #hist_item = cv2.calcHist([im],[ch],None,[100],[-50,50])#Se crea el histograma
        #cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        #hist = np.int32(np.round(hist_item))
       # plt.plot(bins,hist_item,col)
    plt.show()


def get_image(video):
    """ Funcion que permite obtener la captura de una imagen de la instancia video"""
    retVal,im = video.read()
    return im


if __name__ == '__main__':
    
    camara = 0
    video = cv2.VideoCapture(camara) #Instancia el objeto que permite capturar video de la camara del pc
    #video.set(cv2.CAP_PROP_FRAME_WIDTH,1280) #Permite configurar el tamaño del video, en este caso HD
    #video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    if not video: # Si no es posible acceder al programa termine el programa
        sys.exit()
        
    for i in range(0,1000): # loop de captura
        imCamara = get_image(video) #llama a la funcion obtener la imagen
        
        imagenesFila = preprocesar_img(imCamara)
        cv2.imshow("CapturaVideo",imagenesFila)
        
        
        if cv2.waitKey(36) == ord('q'): # Espera 10ms si la tecla q es presionada
            break
    video.release()
    cv2.destroyAllWindows()
    
    


