
#FAI FINAL 
# AI used to find dense areas in a city by looking at images, then if possible
#Connecting the most dense areas in the most efficient way.


#Rodolfo de la O
#

import cv2
import numpy as np

# Cargar la imagen del mapa
imagen_mapa = cv2.imread("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")
#imagen_mapa = cv2.imread("C:\\Users\\fodel\\OneDrive\\Escritorio\\toma1_lerma.png")


# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen_mapa, cv2.COLOR_BGR2GRAY)

# Aplicar umbral para identificar elementos (casas, calles, etc.)
_, imagen_umbral = cv2.threshold(imagen_gris, 150, 255, cv2.THRESH_BINARY)

# Encontrar contornos en la imagen umbral
contornos, _ = cv2.findContours(imagen_umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos en la imagen original
cv2.drawContours(imagen_mapa, contornos, -1, (0, 255, 0), 2)

# Calcular la densidad de contornos por área y encontrar regiones densas
umbral_densidad = 8  # Aumentar densidad a voluntad #Lerma funciono 15
                    #Parece ser que densidad para todo TOLUCA sirve 6 maso menos.


regiones_densas = []
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 0:
        densidad = len(contorno) / area
        if densidad > umbral_densidad:
            regiones_densas.append(contorno)

# Dibujar círculos rojos en las zonas densas
for contorno_denso in regiones_densas:
    momento = cv2.moments(contorno_denso)
    if momento["m00"] != 0:
        centro_x = int(momento["m10"] / momento["m00"])
        centro_y = int(momento["m01"] / momento["m00"])

        # Crear un contorno que represente un círculo
        radio = 30 #Radio para lerma funciono 70
                #Valor para Toluca va a ser 30 parece ser maso menos
        contorno_circulo = np.array([[
            (centro_x + int(radio * np.cos(theta)), centro_y + int(radio * np.sin(theta)))
            for theta in np.linspace(0, 2 * np.pi, 100)
        ]], dtype=np.int32)

        # Dibujar el contorno del círculo
        cv2.drawContours(imagen_mapa, [contorno_circulo], 0, (0, 0, 255), 2) #El ultimo valor es para el volumen del diametro en Lerma funciona 3
                                                                             #El valor para toluca puede ser 2

# Mostrar la imagen con contornos
cv2.imshow("Mapa con Contornos", imagen_mapa)
cv2.waitKey(0)
cv2.destroyAllWindows()


