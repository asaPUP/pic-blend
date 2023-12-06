from flask import Flask, render_template, request, redirect, url_for, session, abort
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os
from functions import get_backgrounds, get_gallery, generate_image, send_email_message, send_whatsapp_message
from werkzeug.utils import secure_filename
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/sistemin.db')

app = Flask(__name__)

app.secret_key = 'Cambiar esta llave si nos vamos a producción en algún punto jjj'

# Configuración de la carpeta de subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'static/uploads')

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
def procesar_imagen(background_id):                 # NOTA: ESTO DEBERÍA SER CAMBIADO A "SUBIR IMAGEN" O ALGO ASÍ
    if background_id == None:
        return "No se ha seleccionado un fondo válido."
    
    return render_template('process_image.html', background_id=background_id)

@app.route('/procesar-imagen', methods=['POST'])
def posicionar_imagen():
    if 'imagen' not in request.files:
        return "No se ha cargado una imagen válida."

    uploaded_image = request.files['imagen']
    img_filename = secure_filename(uploaded_image.filename)
    uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'tmp/{img_filename}'))


    session['up_image_filename'] = img_filename
    selected_bg_id = request.form['background_id']

    return render_template('position.html', bg_id=selected_bg_id)

@app.route('/process-image', methods=['POST'])
def process_image():
    temp_images_directory = os.path.join(app.config['UPLOAD_FOLDER'] + '/tmp')

    if os.listdir(temp_images_directory) == None:
        return "404 not found"

    uploaded_id = generate_image(app, request, session)

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

@app.route('/enviar/<int:id>')
def enviar_correo(id):
    receiver_email = request.args.get('email')
    url = request.url_root + "resultado/" + str(id)

    # Enviar correo electrónico en un hilo separado
    thread = threading.Thread(target=send_email_message, args=(receiver_email, url))
    thread.start()

    # Redirigir a la página de resultado
    return redirect(url_for('resultado', id=id))

# Para iniciar el servidor de pruebas, usar:
#  $ flask run
#  $ flask --debug run (para iniciarlo en modo de depuración)
#  IMPORTANTE: Ejecutar antes de todo en el server "$ sudo xhost +" para permitir el acceso a la pantalla con pywhatkit