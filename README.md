
# PicBlend

PicBlend is a Flask-based web application designed to streamline the process of blending images. With PicBlend, users can seamlessly remove the background of an image and overlay it onto a new background selected from an internal gallery.

Additionally, PicBlend offers features such as generating a QR code for the resulting picture and enabling users to share the link via Email and WhatsApp, simplifying the process of sharing their creations.

## Features:

- Select images from a library of backgrounds.
- Upload images from your computer to overlay on selected backgrounds.
- Automatic QR code generation for the result.
- Options to download generated images, or send them via email and WhatsApp.
- Intuitive and user-friendly interface.

## Technologies Used:

- **Python 3.11**
- **Flask Framework**
- **Pillow** (Python Imaging Library)
- **rembg** (Background Removal Tool)
- **SQLite** (Database Management)
- **Werkzeug** (WSGI Utility Library)
- **SMTP** (Email Sending)
- **SSL** (Secure Sockets Layer)
- **email.mime** (MIME Email Formatting)
- **threading** (Multithreading)
- **pywhatkit** (WhatsApp Automation)

## Usage:

### Installation:

To set up the project, you'll need Python 3.11.x. Start by **creating a virtual environment** within the project directory.

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate`
```

Then, install the **required dependencies**:

`$ python3 -m pip install -r requirements.txt`

### Running the Application:

Once the dependencies are installed, **execute** the Flask app:

```bash
$ export FLASK_APP=app.py
$ flask run`
```

**Navigate** to the provided address in your browser to access the application.

### Deactivating the Virtual Environment:

To **deactivate** the virtual environment, simply run:

`$ deactivate`

## Starting the Development Server:

To start the development server, use:

```bash
$ flask run
$ flask --debug run  # (to start it in debug mode)
```

**IMPORTANT:** Run `$ sudo xhost +` before running the server to allow access to the screen with pywhatkit.

## Contributing:

Contributions to PicBlend are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -am 'Add some amazing feature'`).
4. Push your branch to your fork (`git push origin feature/AmazingFeature`).
5. Open a pull request.
