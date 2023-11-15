from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os
import segno

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/sistemin.db')

app = Flask(__name__)

# Configuración de la carpeta de subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'static/uploads')

# Funcion para obtener el codigo QR de una URL
def get_qr(url):
    qr = segno.make(url)
    qr.save(f'{url}', scale=10, border=0)

# Funcion para obtener las imagenes de background de la base de datos en una tupa (...) de tuplas (id, path)
def get_backgrounds():
    # Obtiene los fondos de la base de datos
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM background')
    backgrounds = cursor.fetchall()
    conn.close()

    return backgrounds # backgrounds es una tupla de tuplas (id, path)

def get_gallery():
    # Obtiene las ultimas 20 imagenes generadas de la base de datos
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generated ORDER BY id DESC LIMIT 20')
    gallery = cursor.fetchall()
    conn.close()

    return gallery # gallery es una tupla de tuplas (id, path)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/crear')
def crear_imagen():
    backgrounds = get_backgrounds()
    return render_template('backgrounds.html', backgrounds=backgrounds)

@app.route('/galeria')
def galeria():
    gallery = get_gallery()
    return render_template('galeria.html', gallery=gallery)

@app.route('/procesar/<int:background_id>')
def procesar_imagen(background_id):
    if background_id == None:
        return "No se ha seleccionado un fondo válido."
    
    return render_template('process_image.html', background_id=background_id)

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
    uploaded_id = cursor.fetchone()[0] # Obtiene el id de la última imagen cargada
    if uploaded_id == None:
        uploaded_id = 0
    uploaded_id += 1 # Incrementa el id para la nueva imagen

    # Guarda la imagen cargada en un archivo temporal
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp{uploaded_id}.png')
    imagen.save(temp_path)

    # Procesa la imagen para eliminar el fondo
    input_image = Image.open(temp_path)
    output_image = remove(input_image)

    # Pega la imagen procesada sobre el fondo seleccionado, con un tamaño que no exceda el del fondo pero que mantenga la relación de aspecto
    background_id = request.form['background_id']
    background_path = os.path.join(current_dir, f'static/img/backgrounds/{background_id}.jpg')

    # Abre la imagen de fondo y obtiene sus dimensiones
    background_image = Image.open(background_path)
    background_width, background_height = background_image.size

    # Obtiene las dimensiones de la imagen de salida (la que se obtiene al eliminar el fondo)
    output_width, output_height = output_image.size
    
    # Redimensiona la imagen de salida si es necesario, dejando un margen de 10px en cada lado
    if output_width > background_width:
        output_image.thumbnail((background_width - 20, background_height), Image.LANCZOS)
        output_width, output_height = output_image.size

    if output_height > background_height:
        output_image.thumbnail((background_width, background_height - 20), Image.LANCZOS)
        output_width, output_height = output_image.size

    # Pega la imagen de salida que tiene el fondo transparente sobre la imagen de fondo, centrada, y dejando 10px de margen
    background_image.paste(output_image, (int((background_width - output_image.size[0]) / 2), int((background_height - output_image.size[1]) / 2)), output_image)

    # Guarda la imagen compuesta en un archivo en la carpeta de subida de archivos 'static/uploads'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uploaded_id}.png')
    background_image.save(output_path)

    relative_path = os.path.join('static', 'uploads', f'{uploaded_id}.png') # Ejemplo: 'static/uploads/1.png

    # Guarda la información de la imagen con fondo en la base de datos con un path relativo
    cursor.execute('INSERT INTO generated (id, path) VALUES (?, ?)', (uploaded_id, relative_path))
    conn.commit()
    conn.close()

    # Limpia el archivo temporal
    os.remove(temp_path)

    return redirect(url_for('resultado', id=uploaded_id))

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