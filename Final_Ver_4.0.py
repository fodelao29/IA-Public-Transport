
import os
import cv2
import numpy as np
import tkinter as tk    
from tkinter import filedialog
from PIL import Image, ImageTk
from sklearn import svm
from skimage.io import imread
from skimage.transform import resize
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
#from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


#TENSORFLOW NOT WORKING ON MY COMPUTER.
# Nota: No aplicar aumento de datos al conjunto de validación
#validation_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)


def read_and_preprocess(image_path):
    img = imread(image_path)               # Lee la imagen en color
    img_resized = resize(img, (50, 50))    # Redimensiona la imagen
    return img_resized.flatten()           # Aplana la imagen a 1D

# Cargar imágenes
folder_high_density = 'D:/Users/fodel/Escritorio/Python Practice Kyoto/FINAL_IA/Images/dats_set/high_density'
folder_low_density = 'D:/Users/fodel/Escritorio/Python Practice Kyoto/FINAL_IA/Images/dats_set/low_density'

# Etiquetas: 1 para alta densidad, 0 para baja densidad
data = [read_and_preprocess(os.path.join(folder_high_density, file)) for file in os.listdir(folder_high_density)] + \
       [read_and_preprocess(os.path.join(folder_low_density, file)) for file in os.listdir(folder_low_density)]

labels = [1] * len(os.listdir(folder_high_density)) + [0] * len(os.listdir(folder_low_density))
#label_text =  ["HIGH DENSITY", "LOW DENSITY"][labels]

# Crear y entrenar el clasificador
clf = svm.SVC()
clf.fit(data, labels)


#imagen_mapa = cv2.imread("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")
# () SHOULD BE RUTA_IMAGEN 
def procesar_imagen(ruta_imagen,canvas_imagen): #
        imagen_mapa = cv2.imread(ruta_imagen)  #("C:\\Users\\fodel\\OneDrive\\Escritorio\\mapa_toluca_tomaaerea.png")

        # Convertir la imagen a escala de grises
        imagen_gris = cv2.cvtColor(imagen_mapa, cv2.COLOR_BGR2GRAY)

        # Convertir la imagen a espacio de color HSV
        imagen_hsv = cv2.cvtColor(imagen_mapa, cv2.COLOR_BGR2HSV)

        # Aplicar umbral para identificar elementos (casas, calles, etc.)
        # _, imagen_umbral = cv2.threshold(imagen_gris, 150, 255, cv2.THRESH_BINARY)

        # Definir el rango de color amarillo en HSV
        # Estos valores pueden necesitar ajustes
        amarillo_bajo = np.array([10, 100, 100], dtype=np.uint8) #10,100,100
        amarillo_alto = np.array([33, 255, 255], dtype=np.uint8) #30,255,255

        mascara_amarilla = cv2.inRange(imagen_hsv, amarillo_bajo, amarillo_alto)

        contornos, _ = cv2.findContours(mascara_amarilla, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Encontrar contornos en la imagen umbral
        contornos, _ = cv2.findContours(mascara_amarilla, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # Filtrar contornos por área - suponiendo que las áreas más grandes son más densas
        contornos_densos = [c for c in contornos if cv2.contourArea(c) > 50]  # Área mínima ajustable

        # Dibujar contornos en la imagen original
        cv2.drawContours(imagen_mapa, contornos_densos, -1, (0, 255, 0), 2)

        # Calcular la densidad de contornos por área y encontrar regiones densas
        umbral_densidad = 20  # Aumentar densidad a voluntad #Lerma funciono 15
                            #Parece ser que densidad para todo TOLUCA sirve 6-8 maso menos.


        centros_densos = []
        

        # Dibujar círculos rojos en las zonas densas
        for contorno in contornos_densos:
            M = cv2.moments(contorno)
            if M["m00"] != 0:
                centro_x = int(M["m10"] / M["m00"])
                centro_y = int(M["m01"] / M["m00"])
                centros_densos.append((centro_x, centro_y))
                cv2.circle(imagen_mapa, (centro_x, centro_y), 10, (0, 0, 255), -1)

        # Dibujar líneas entre los centros de los contornos densos
        for i in range(len(centros_densos) - 1):
            cv2.line(imagen_mapa, centros_densos[i], centros_densos[i + 1], (255, 0, 0), 2)

    
       
        flattened_image = read_and_preprocess(ruta_imagen)
        density_prediction = clf.predict([flattened_image])[0]

        # Definir el texto según la predicción de densidad
        if density_prediction == 1:
             texto = "High Density"
        else:
              texto = "Low Density"


        # Agregar texto a la imagen
        posicion = (50, 50)  # Coordenadas (x, y) donde se colocará el texto
        fuente = cv2.FONT_HERSHEY_SIMPLEX
        escala = 1
        color = (0, 0, 255)  # Color en formato BGR (azul, verde, rojo)
        grosor = 2

        cv2.putText(imagen_mapa, texto, posicion, fuente, escala, color, grosor)
        # Convertir la imagen OpenCV a formato PIL para mostrar en el canvas
        imagen_pil = Image.fromarray(cv2.cvtColor(imagen_mapa, cv2.COLOR_BGR2RGB))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)

        # Mostrar la imagen en el canvas
        canvas_imagen.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
        canvas_imagen.image = imagen_tk  #

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
ventana.title("AI Model Density Predicter")

# Botón para seleccionar imagen
btn_seleccionar = tk.Button(ventana, text="Choose Image", command=lambda: seleccionar_imagen(canvas_imagen)) #Using lambda functionwill let us have any number input parameters
btn_seleccionar.pack(pady=10)

# Canvas para mostrar la imagen procesada
canvas_imagen = tk.Canvas(ventana, width=500, height=500)
canvas_imagen.pack()


    
ventana.mainloop()

