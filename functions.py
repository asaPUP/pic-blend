import sqlite3
import os
import sys
import subprocess
from PIL import Image, ImageOps
from rembg import remove

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/sistemin.db')

# Funcion para obtener las imagenes de background de la base de datos en una tupla (...) de tuplas (id, path)
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

def generate_image(app, request, session):
    # Asigna un nombre único a la imagen cargada, obtenido del id en la base de datos
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM generated')
    uploaded_id = cursor.fetchone()[0] # Obtiene el id de la última imagen cargada
    if uploaded_id == None:
        uploaded_id = 0
    uploaded_id += 1 # Incrementa el id para la nueva imagen

    # Guarda la imagen cargada en un archivo temporal (AHORA LA IMAGEN YA ESTÁ CARGADA DESDE ANTES)
    #temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp{uploaded_id}.png')
    #imagen.save(temp_path)

    # Procesa la imagen para eliminar el fondo
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"tmp/{session['up_image_filename']}")
    input_image = Image.open(temp_path)
    

    # Pega la imagen procesada sobre el fondo seleccionado, con un tamaño que no exceda el del fondo pero que mantenga la relación de aspecto
    background_id = request.form['background-id']
    background_path = os.path.join(current_dir, f'static/img/backgrounds/{background_id}.jpg')

    # Abre la imagen de fondo y obtiene sus dimensiones
    background_image = Image.open(background_path)
    bg_width, bg_height = background_image.size
    if (bg_width < 500 and bg_height < 500):
        background_image.thumbnail((500, 500), Image.Resampling.LANCZOS)
    
    background_width, background_height = background_image.size
    output_image = remove(input_image)
    output_image.thumbnail((background_width / 4, background_height / 4), Image.Resampling.LANCZOS)

    # Obtiene las dimensiones de la imagen de salida (la que se obtiene al eliminar el fondo)
    #output_width, output_height = output_image.size
    
    # Redimensiona la imagen de salida si es necesario, dejando un margen de 10px en cada lado
    # if output_width > background_width:
    #     output_image.thumbnail((background_width - 20, background_height), Image.LANCZOS)
    #     output_width, output_height = output_image.size

    # if output_height > background_height:
    #     output_image.thumbnail((background_width, background_height - 20), Image.LANCZOS)
    #     output_width, output_height = output_image.size

    # Pega la imagen de salida que tiene el fondo transparente sobre la imagen de fondo, centrada, y dejando 10px de margen
    #background_image.paste(output_image, (int((background_width - output_image.size[0]) / 2), int((background_height - output_image.size[1]) / 2)), output_image)
    x, y = (int(request.form['x']), int(request.form['y']))

    if (bg_width < 500 and bg_height < 500):
        background_image.paste(output_image, (int(x / 1.7), int(y / 1.7)), output_image)
    elif (abs(bg_width - bg_height) < 50):
        background_image.paste(output_image, (int(x), int(y)), output_image)
    else:
        background_image.paste(output_image, (int(x*2), int(y*2)), output_image)


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

    return uploaded_id

def send_email_message(receiver_email, url): # receiver_email debe tener el formato "nombre@dominio.com"
    print("Entro a la funcion send_email_message")

    print(f"Receptor: {receiver_email}")
    print(f"URL: {url}")

    print("Saliendo de la funcion send_email_message")

    python_interpreter = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
    subprocess.run([python_interpreter, 'emailmessage.py', receiver_email, url])

def send_whatsapp_message(phone_number, url): # phone?number debe tener el formato "+00 123 456 7890"
    python_interpreter = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
    subprocess.run([python_interpreter, 'whatsappmessage.py', phone_number, url])