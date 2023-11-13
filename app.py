from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os

app = Flask(__name__)


 

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/procesar', methods=['POST'])
def procesar_imagen():
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            # Guarda la imagen cargada en un archivo temporal
            temp_path = 'temp.png'
            imagen.save(temp_path)

            # Procesa la imagen para eliminar el fondo
            input_image = Image.open(temp_path)
            output_image = remove(input_image)

            # Guarda la imagen procesada en la carpeta 'static'
            output_path = 'static/imagen_procesada.png'
            output_image.save(output_path)

            # Limpia el archivo temporal
            os.remove(temp_path)

            return render_template('resultado.html')
    return "No se ha cargado una imagen válida."

if __name__ == '__main__':
    app.run()
