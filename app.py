from flask import Flask, render_template, request, redirect, url_for, session, abort
from PIL import Image, ImageOps
from rembg import remove
import sqlite3
import os
from functions import get_backgrounds, get_gallery, generate_image, send_email_message, send_whatsapp_message
from werkzeug.utils import secure_filename
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/pic-blend.db')

app = Flask(__name__)

app.secret_key = 'Change this key if we go into production at any point lol'

# Configuration for the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'static/uploads')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/create')
def create_image():
    backgrounds = get_backgrounds()
    return render_template('backgrounds.html', backgrounds=backgrounds)


@app.route('/gallery')
def gallery():
    gallery = get_gallery()
    return render_template('gallery.html', gallery=gallery)


@app.route('/process/<int:background_id>')
def process_image(background_id):  # NOTE: THIS SHOULD BE RENAMED TO "UPLOAD IMAGE" OR SOMETHING SIMILAR
    if background_id is None:
        return "No valid background selected."
    
    return render_template('process_image.html', background_id=background_id)


@app.route('/process-image', methods=['POST'])
def position_image():
    if 'image' not in request.files:
        return "No valid image uploaded."

    uploaded_image = request.files['image']
    img_filename = secure_filename(uploaded_image.filename)
    uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'tmp/{img_filename}'))

    session['up_image_filename'] = img_filename
    selected_bg_id = request.form['background_id']

    return render_template('position.html', bg_id=selected_bg_id)


@app.route('/process-image-helper', methods=['POST'])
def process_image_helper():
    temp_images_directory = os.path.join(app.config['UPLOAD_FOLDER'] + '/tmp')

    if not os.listdir(temp_images_directory):
        return "404 not found"

    uploaded_id = generate_image(app, request, session)

    return redirect(url_for('result', id=uploaded_id))


@app.route('/result/<int:id>')
def result(id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generated WHERE id = ?', (id,))
    image = cursor.fetchone()
    conn.close()

    if not image:
        return "Requested image not found."
    
    return render_template('result.html', image=image)  # image is a tuple with image data (id, relative_path)


@app.route('/send/<int:id>')
def send_email(id):
    receiver_email = request.args.get('email')
    url = request.url_root + "result/" + str(id)

    # Sending email in a separate thread
    thread = threading.Thread(target=send_email_message, args=(receiver_email, url))
    thread.start()

    # Redirect to the result page
    return redirect(url_for('result', id=id))

@app.route('/send-wa/<int:id>')
def send_wa_message(id):
    receiver_phone = request.args.get('phone')
    url = request.url_root + "result/" + str(id)

    # Sending WhatsApp message in a separate thread
    thread = threading.Thread(target=send_whatsapp_message, args=(receiver_phone, url))
    thread.start()

    # Redirect to the result page
    return redirect(url_for('result', id=id))


# To start the development server, use:
#  $ flask run
#  $ flask --debug run (to start it in debug mode)
#  IMPORTANT: Run "$ sudo xhost +" on the server first to allow access to the screen with pywhatkit
