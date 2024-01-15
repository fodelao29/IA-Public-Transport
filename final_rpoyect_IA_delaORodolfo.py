#FAI FINAL 
# AI used to find dense areas in a city by looking at images, then if possible
#Connecting the most dense areas in the most efficient way.

#Rodolfo de la O

import cv2
import numpy as np
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

imagen_mapa = cv2.imread("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")
# () SHOULD BE RUTA_IMAGEN 
def procesar_imagen(imagen_mapa,canvas_imagen):
        imagen_mapa = cv2.imread(imagen_mapa)  #("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")

        # Cargar la imagen del mapa
        #imagen_mapa = cv2.imread("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")
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


        # Dibujar línea que conecta los centros
        #Dibujar lineas entre ciruclos, despues hay que utilizar el algoritmo de djastra para hacerlo de manera correct ay eficiente.
        for i in range(len(regiones_densas) - 1):
            centro_1 = cv2.moments(regiones_densas[i])["m10"] / cv2.moments(regiones_densas[i])["m00"], cv2.moments(regiones_densas[i])["m01"] / cv2.moments(regiones_densas[i])["m00"]
            centro_2 = cv2.moments(regiones_densas[i + 1])["m10"] / cv2.moments(regiones_densas[i + 1])["m00"], cv2.moments(regiones_densas[i + 1])["m01"] / cv2.moments(regiones_densas[i + 1])["m00"]
            
            # Dibujar línea que conecta los centros
            cv2.line(imagen_mapa, (int(centro_1[0]), int(centro_1[1])), (int(centro_2[0]), int(centro_2[1])), (255, 0, 0), 2)


        # Calcular y dibujar líneas que conectan círculos cercanos
        umbral_distancia = 100  # Puedes ajustar este umbral según sea necesario

        for i in range(len(regiones_densas) - 1):
            centro_1 = cv2.moments(regiones_densas[i])["m10"] / cv2.moments(regiones_densas[i])["m00"], cv2.moments(regiones_densas[i])["m01"] / cv2.moments(regiones_densas[i])["m00"]
            
            for j in range(i + 1, len(regiones_densas)):
                centro_2 = cv2.moments(regiones_densas[j])["m10"] / cv2.moments(regiones_densas[j])["m00"], cv2.moments(regiones_densas[j])["m01"] / cv2.moments(regiones_densas[j])["m00"]
                
                # Calcular la distancia entre los centros
                distancia = np.sqrt((centro_1[0] - centro_2[0]) ** 2 + (centro_1[1] - centro_2[1]) ** 2)
                
                # Conectar círculos cercanos
                if distancia < umbral_distancia:
                    cv2.line(imagen_mapa, (int(centro_1[0]), int(centro_1[1])), (int(centro_2[0]), int(centro_2[1])), (255, 0, 0), 2)



        # Mostrar la imagen con contornos
        cv2.imshow("Mapa con Contornos", imagen_mapa)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

pass

def seleccionar_imagen(canvas_imagen):
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
    
    if ruta_imagen:
        procesar_imagen(ruta_imagen, canvas_imagen)

#Showing Window
ventana = tk.Tk()
ventana.title("Procesador de Imágenes")

# Botón para seleccionar imagen
btn_seleccionar = tk.Button(ventana, text="Seleccionar Imagen", command=lambda: seleccionar_imagen(canvas_imagen)) #Using lambda functionwill let us have any number input parameters
btn_seleccionar.pack(pady=10)

# Canvas para mostrar la imagen procesada
canvas_imagen = tk.Canvas(ventana, width=1000, height=1000)
canvas_imagen.pack()


#AQUI SELECCIONAMOS LA IMAGEN Y AGREGAMOS CANVAS_IMAGEN PARA QUE NO CREE UN CANVAS NUEVO Y NOS MUESTRE EL RESULTADO
# EN EL CANVAS YA EXISTENTE
#def seleccionar_imagen(canvas_imagen):
#    ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
#    
#    if ruta_imagen:
#        procesar_imagen(ruta_imagen, canvas_imagen)

# Función para actualizar el canvas con la imagen procesada
def actualizar_canvas(imagen_cv2, canvas_imagen):
    imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
    imagen_pil = Image.fromarray(imagen_rgb)
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    canvas_imagen.config(width=imagen_tk.width(), height=imagen_tk.height())
    canvas_imagen.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
    canvas_imagen.imagen_tk = imagen_tk  # Guardar una referencia para evitar la recolección de basura
    cv2.imshow("Mapa con Contornos", imagen_mapa)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Mostrar la ventana
ventana.mainloop()




