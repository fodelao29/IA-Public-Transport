
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

