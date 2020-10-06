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
    imagenLABColor = cv2.cvtColor(imagen,cv2.COLOR_BGR2LAB)
    #imagenGray3Ch = cv2.merge((imagenGray,imagenGray,imagenGray)) #Permite juntar las 3 capas en una imagen de 3 canales
    #hist_curve_alt(imagenProcesada)
    filtroL = imagenLABColor[:,:,0] < 115 #Filtro para no dejar pasar valores por debajo en L
    imagenProcesada[filtroL] = 0
    filtroA = imagenLABColor[:,:,1] < 80.4  #Filtro para no dejar pasar valor por debajo en A
    imagenProcesada[filtroA] = 0
    filtroB = imagenLABColor[:,:,2] < 170 # Filtro para no dejar pasar valores por debajo en B
    imagenProcesada[filtroB] = 0
    
    """Operaciones morfologicas"""
    ventanaDeslizante = np.ones((3,3),np.uint8)
    imagenProcesada = cv2.dilate(imagenProcesada,ventanaDeslizante);
    #Se eliminina los huecos negros producidos por las letras del marcador
    imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_OPEN, ventanaDeslizante)  #transformacion open, se realiza primero erosion y luego dilatacion
    #imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_OPEN, ventanaDeslizante)
    #ventanaDeslizante = np.ones((12,12),np.uint8)
    #imagenProcesada = cv2.morphologyEx(imagenProcesada, cv2.MORPH_CLOSE, ventanaDeslizante) 
    
    
    imagen[imagenProcesada == 0] = 0
    
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
    
    
    return imagen
    
    
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
    video.set(cv2.CAP_PROP_FRAME_WIDTH,1280) #Permite configurar el tamaño del video, en este caso HD
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    if not video: # Si no es posible acceder al programa termine el programa
        sys.exit()
        
    for i in range(0,100000): # loop de captura
        imCamara = get_image(video) #llama a la funcion obtener la imagen
        
        imagenesFila = preprocesar_img(imCamara)
        cv2.imshow("CapturaVideo",imagenesFila)
        
        
        if cv2.waitKey(36) == ord('q'): # Espera 10ms si la tecla q es presionada
            break
    video.release()
    cv2.destroyAllWindows()
    
    


