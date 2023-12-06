from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os
from functions import get_backgrounds, get_gallery, generate_image, send_email_message, send_whatsapp_message
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/sistemin.db')

app = Flask(__name__)

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
    
    uploaded_id = generate_image(app, request, imagen)

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

# Ruta para enviar un correo electrónico <url>/enviar/<id>?email=<email> # Ejemplo: http://localhost:5000/enviar/1?email=correo@dominio.com
@app.route('/enviar/<int:id>')
def enviar_correo(id):
    receiver_email = request.args.get('email')
    url = request.url_root + url_for('resultado', id=id)

    # Enviar correo electrónico en un hilo separado
    import threading
    thread = threading.Thread(target=send_email_message, args=(receiver_email, url))
    thread.start()

    return redirect(url_for('resultado', id=id))


# Para iniciar el servidor de pruebas, usar:
#  $ flask run
#  $ flask --debug run (para iniciarlo en modo de depuración)