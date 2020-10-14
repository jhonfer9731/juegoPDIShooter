# -*- coding: utf-8 -*-
"""---------------------------------------------------------------------------
------------------------------------------------------------------------------
-------------------PROCESAMIENTO DIGITAL DE IMAGENES--------------------------
---------------------FUNCIONES PDI SHOOTER-MASTER-----------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
----Por: CHRISTIAN CAMILO GARZÓN VÁSQUEZ y JHON FERNANDO BENAVIDES BASTIDAS---
----CC: ---------- 1037637207 ------------------- 1087618855 -----------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------UNIVERSIDAD DE ANTIOQUIA -----------------------------
-------------------------FACULTAD DE INGENIERIA-------------------------------
-----------------INGENIERIA ELECTRONICA Y DE TELECOMUNICACIONES---------------
-------------------------------2020-1-----------------------------------------
---------------------------------------------------------------------------"""


"""---------------------------------------------------------------------------
Se añaden las libreberias necesarias para el procesamiento digital de las 
imagenes, tales como OpenCV (cv2) y Numpy (np), además de inicializar el video
y centroide.
---------------------------------------------------------------------------"""

from cv2 import * #Uso de libreria OpenCv
import numpy as np #Uso de libreria NumPy

camara = 0   #Se inicial la camara, por defecto es 0
video = cv2.VideoCapture(camara) #Se inicia la captura de video
coordenadasCentroide = [0,0] #Se inicializa la tupla para el centroide
cX = 0 #Coordenada en X del centroide
cY = 0 #Coordenada en y del centroide

"""---------------------------------------------------------------------------
Con la función get_image que retorna el frame de la imagen actual de la 
camara web.
---------------------------------------------------------------------------"""

def get_image(): #Sin parametro de entrada
    
     retval, im = video.read() #Se inica la lectura del video frame por frame
     return im #retorno de la imagen capturada
 
"""---------------------------------------------------------------------------
 Con la función normi que tiene como parametro una componente de imagen, se 
 procesa para entregar la componente normalizada
---------------------------------------------------------------------------"""
 
def normi(compo): #Componente de imagen como parametro
    
    compo = compo.astype(np.float64) #Se convierte de base8 a double la matriz
    compo = compo/np.max(compo) #Se normaliza la componente
    compo = 255 * compo #Se multiplica por 255 para conservar valores de base8
    compo = compo.astype('uint8') #Se convierte de nuevo a base8
    
    return compo #Se retorna componente normalizada y en base8
 
"""---------------------------------------------------------------------------
 Con la función componente_lab,con parametro de entrada un snap, se extrae la
 componente requerida, además de hacer un filtrado de los niveles de intesidad
 requeridos en las componentes A y B siendo binarizados con niveles 0 o 255
 y retornado el resultado
---------------------------------------------------------------------------"""    
    
def componente_lab(snap):
    
    cero = np.uint8(0) #Valor 0 en tipo base8
    d55 = np.uint8(255) #Valor 255 en tipo base8
    snap_lab = cvtColor(snap, COLOR_BGR2LAB) # Usando CV2, cambia de espacio de color desde RGB a LAB
    snap_b = snap_lab[:,:,2] # 0->L 1->A 2->B por pre-procesado se escoge B
    snap_a = snap_lab[:,:,1] # 0->L 1->A 2->B por pre-procesado se escoge A
    snap_bn = np.where(snap_b>170,d55,cero) #Se filtra según nivel requerido según ambiente y visualización
    snap_bn[snap_a > 200] = 0 # filtro en a para que la imagen no se contamine en condicion nocturna
    
    return snap_bn #Se retorna la componente b filtrada

"""---------------------------------------------------------------------------
Con la función openf,se realiza operación de apertura al parametro de entrada,
teniendo con fin eliminar ruido en el entorno del objeto como elemento
estructurante se usa un cuadrado de 2x2 ya que al pre-procesar se dio como la
mejor opción. La apertura se da con varias erosiones y varias dilataciones.
La salida es la componente con las operaciones indicadas.
---------------------------------------------------------------------------"""

def openf(compo):
    
    ee = np.ones((2,2),np.uint8)    #Elemento estructurante
    imagenProcesada = cv2.morphologyEx(compo, cv2.MORPH_OPEN, ee, iterations=5) #Aplicación del open 5 veces 
    imagenProcesada = cv2.dilate(compo,ee,iterations = 3) #3 dilataciones

    return  imagenProcesada #Retornar componente tras proceso de apertura

"""---------------------------------------------------------------------------
Con la función mask, cuyos parametros de entrada serán la imagen pre-procesada
y sus dimensiones. Se tendrá en cuenta aquellos valores donde el objeto de 
interés se encuentre presente frente a la camara con cierta cantidad de pixeles.
De allí se definen dos zonas de control respecto a las dimensiones orginales.
Se pasa a un proceso de binarización de la imagen con el fin de hallar el
contorno de está, necesitando de una operación para encontrar el porcentaje de
concavidad entre los dedos y de esta manera detectar si hay un cierre o 
apertura de la mano. También se aplica la busqueda del centroide del contorno,
esto con el fin de hallar su tendencia a una u otra región de movimiento
tanto en x como y. Al final respecto a ciertos porcentajes impuestos se 
determina una u otra región y si hay apertura de los dedos.
---------------------------------------------------------------------------"""

def masks(im,screenSize):
    #the shape of the image is (height,width)
    width = screenSize[0] #Ancho de la imagen
    height = screenSize[1] #Alto de la imagen
    total = im.shape[0] * im.shape[1] #Numero de pixeles de la imagen original
    count = cv2.countNonZero(im) #Numero de pixeles del objeto en la imagen originalm no cero.
    
    if count < 11000:  #Comprueba que el objeto sea visible, estableciendo un limite (cantidad de pixeles) inferior para los controles
        return (0,0,im)


    """Definición de las regiones de decision para el movimiento de la nave"""
    ml = im[:,250:445] #Region para moverse a la izquierda
    total_ml = ml.shape[0] * ml.shape[1] #dimension total de la region de decision para mov a izquierda
    count_ml = cv2.countNonZero(ml) #Area total ocupada por el objeto dentro de la region de decision
    
    mr = im[:,445:640] #Region para moverse a la derecha
    total_mr = mr.shape[0] * mr.shape[1] #dimension total de la region de decision para mov a derecha
    count_mr = cv2.countNonZero(mr) #Area total ocupada por el objeto dentro de la region de decision
    
    
    """Binarizacion de la imagen"""
    ret,thresh = cv2.threshold(im,127,255,0) #Se binariza la imagen para obtener los contornos con el fin de hallar el centroide y el hull
    
    
    """Calculo del contorno de la mano del jugador"""
    puntosContorno = encontrarContornos(thresh) #Busca lista de contornos
    areaContorno = cv2.contourArea(puntosContorno) #Area del contorno mayor
    imConContorno = cv2.drawContours(cv2.merge([im,im,im]), [puntosContorno], -1, (0,255,100), 3) #Imagen con puntos del cortorno IMG/CONTORNO/PARAMETRO/COLOR/GRUESO
    
    hull = cv2.convexHull(puntosContorno) # Encuentra los Convexity deflects, cuyo contorno ajusta y une las concavidades entre las puntas de los dedos
    imConContorno = cv2.drawContours(imConContorno, [hull], -1, (0,0,255), 3) #Dibuja el contorno encontrado por convexHull
    areaConvexHull = cv2.contourArea(hull) #Area del contorno ajustado
    
    
    """Calculo del area entre los dedos de la mano (espacios de deflexion de la concavidad) """
    areaEntreDedos = areaConvexHull-areaContorno #Area de las concavidades de los dedos
    
    if areaConvexHull != 0: 
        porcAreaEntreDedos = areaEntreDedos*100/areaConvexHull #Que tanto abre o cierra los dedos
    else:
        porcAreaEntreDedos = 0


    """Calulo del centroide de la imagen """
    
    M = cv2.moments(puntosContorno) #Calculo de los momentos de la imagen según el contorno. Entrega lista de los momentos estadisticos de la imagen
    if(M["m00"] != 0) :
        cX = int(M["m10"] / M["m00"]) #M00: Area, INT M10:X*F(XY)
        cY = int(M["m01"] / M["m00"]) #M00: Area, INT M10:Y*F(XY)

    coordenadasCentroide[0] = cX #Coordenadas en X
    coordenadasCentroide[1] = cY #Coordenadas en Y
    
    
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

"""---------------------------------------------------------------------------
Como parametro de entrada se da la imagen binarizada, su fin es buscar todos los
contorno punto a punto verificando si es borde. Entrega una lista con aquellos
puntos x,y donde estan los bordes de los objetos y elige el de mayor área para
enviar.
---------------------------------------------------------------------------"""

def encontrarContornos(imagenBW):

    contornos,hierarchy = cv2.findContours(imagenBW,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    areas = np.array([cv2.contourArea(i) for i in contornos])
    indiceMaxContour = np.argmax(areas) #Se envia el contorno de la mano, representnado el area maxima
    
    return contornos[indiceMaxContour]
    
"""---------------------------------------------------------------------------
La función loopImagen logra capturar frame por frame, donde a cada frame
entregado se le procesa con las funciones anteriores. Sacando la
componente, hace una apertura y por ultimo aplica las mascaras para calcular,
su posición y que tanto valor diferente de cero tiene. Se retorna el control
de movimiento y el control del dispositivo.
---------------------------------------------------------------------------"""

def loopImagen():
    
    HEIGHT = 480 #Altura de la imagen
    WIDTH = 640 #Ancho de la imagen
    img = get_image() #Se obtiene un frame del video
    cb = componente_lab(img) #Extracción de la componente a trabajar
    cbd = openf(cb) #Se hace un proceso de apertura
    (controlMov,controlDisp,imagenContornos) = masks(cbd,screenSize=(WIDTH,HEIGHT))
    cv2.imshow("camara_bn", imagenContornos)#Se muestra la imagen prepocesada y segmentada en el espacio LAB junto con sus contornos
    
    return (controlMov,controlDisp) #Retorno de controles

"""---------------------------------------------------------------------------
 La función cerrarVideo se encarga de cancelar y parar el uso de la webcam,
 además de cerrar las ventanas abiertas por la libreria openCV
---------------------------------------------------------------------------"""
   
def cerrarVideo():
    
    video.release()#Se cierra la camara
    cv2.destroyAllWindows()



    