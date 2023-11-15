from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/sistemin.db')

app = Flask(__name__)

# Configuración de la carpeta de subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'static/uploads')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/procesar')
def procesar_imagen():
    return render_template('process_image.html')

@app.route('/procesar-imagen', methods=['POST'])
def _procesar_imagen():
    if 'imagen' not in request.files:
        return "No se ha cargado una imagen válida."
    
    imagen = request.files['imagen']

    if imagen.filename == '':
        return "No se ha cargado una imagen válida."
    
    # Asigna un nombre único a la imagen cargada, obtenido del id en la base de datos
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM generated')
    id = cursor.fetchone()[0]
    if id == None:
        id = 0
    id += 1

    # Guarda la imagen cargada en un archivo temporal
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp{id}.png')
    imagen.save(temp_path)

    # Procesa la imagen para eliminar el fondo
    input_image = Image.open(temp_path)
    output_image = remove(input_image)

    # Guarda la imagen procesada en la carpeta 'static'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{id}.png')
    output_image.save(output_path)

    relative_path = os.path.join('static', 'uploads', f'{id}.png') # Ejemplo: 'static/uploads/1.png

    # Guarda la información de la imagen en la base de datos con un path relativo
    cursor.execute('INSERT INTO generated (id, path) VALUES (?, ?)', (id, relative_path))
    conn.commit()
    conn.close()

    # Limpia el archivo temporal
    os.remove(temp_path)

    return redirect(url_for('resultado', id=id))

@app.route('/resultado/<int:id>')
def resultado(id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generated WHERE id = ?', (id,))
    image = cursor.fetchone()
    conn.close()

    if image == None:
        return "No se ha encontrado la imagen solicitada."
    
    return render_template('resultado.html', image=image) # image es una tupla con los datos de la imagen (id, relative_path)

# Para iniciar el servidor de pruebas, usar:
#  $ flask run
#  $ flask --debug run (para iniciarlo en modo de depuración)