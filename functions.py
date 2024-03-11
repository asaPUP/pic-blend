import sqlite3
import os
import sys
import subprocess
from PIL import Image, ImageOps
from rembg import remove

current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, 'database/pic-blend.db')


# Function to get background images from the database in a tuple (...) of tuples (id, path)
def get_backgrounds():
    # Get backgrounds from the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM background')
    backgrounds = cursor.fetchall()
    conn.close()

    return backgrounds  # backgrounds is a tuple of tuples (id, path)


def get_gallery():
    # Get the last 20 generated images from the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generated ORDER BY id DESC LIMIT 20')
    gallery = cursor.fetchall()
    conn.close()

    return gallery  # gallery is a tuple of tuples (id, path)


def generate_image(app, request, session):
    # Assign a unique name to the uploaded image, obtained from the id in the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM generated')
    uploaded_id = cursor.fetchone()[0]  # Get the id of the last uploaded image
    if uploaded_id is None:
        uploaded_id = 0
    uploaded_id += 1  # Increment the id for the new image

    # Process the image to remove the background
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"tmp/{session['up_image_filename']}")
    input_image = Image.open(temp_path)

    # Paste the processed image onto the selected background, maintaining aspect ratio but not exceeding the background size
    background_id = request.form['background-id']
    background_path = os.path.join(current_dir, f'static/img/backgrounds/{background_id}.jpg')

    # Open the background image and resize it if it is too large
    background_image = Image.open(background_path)
    bg_width, bg_height = background_image.size
    if (bg_width < 500 and bg_height < 500):
        background_image.thumbnail((500, 500), Image.Resampling.LANCZOS)
    
    background_width, background_height = background_image.size
    output_image = remove(input_image)
    output_image.thumbnail((background_width / 4, background_height / 4), Image.Resampling.LANCZOS)

    x, y = (int(request.form['x']), int(request.form['y']))

    if (bg_width < 500 and bg_height < 500):
        background_image.paste(output_image, (int(x / 1.7), int(y / 1.7)), output_image)
    elif (abs(bg_width - bg_height) < 50):
        background_image.paste(output_image, (int(x), int(y)), output_image)
    else:
        background_image.paste(output_image, (int(x*2), int(y*2)), output_image)

    # Save the composed image to a file in the 'static/uploads' folder
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uploaded_id}.png')
    background_image.save(output_path)

    relative_path = os.path.join('static', 'uploads', f'{uploaded_id}.png')  # Example: 'static/uploads/1.png

    # Save the information of the image with background to the database with a relative path
    cursor.execute('INSERT INTO generated (id, path) VALUES (?, ?)', (uploaded_id, relative_path))
    conn.commit()
    conn.close()

    # Clean up the temporary file
    os.remove(temp_path)

    return uploaded_id


def send_email_message(receiver_email, url):  # receiver_email should be in the format "name@domain.com"
    print("Entering send_email_message function")

    print(f"Receiver: {receiver_email}")
    print(f"URL: {url}")

    python_interpreter = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
    subprocess.run([python_interpreter, 'emailmessage.py', receiver_email, url])

    print("Exiting send_email_message function")


def send_whatsapp_message(phone_number, url):  # phone_number should be in the format "+00 123 456 7890"
    print("Entering send_whatsapp_message function")

    print(f"Phone number: {phone_number}")
    print(f"URL: {url}")

    python_interpreter = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
    subprocess.run([python_interpreter, 'whatsappmessage.py', phone_number, url])

    print("Exiting send_whatsapp_message function")
