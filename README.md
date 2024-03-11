# PicBlend

PicBlend is a web application built with Flask that allows users to creatively merge images. Whether you want to overlay an image onto a background, remove backgrounds automatically, or generate a QR code for easy access, PicBlend has you covered.

## Features:

- Select images from a library of backgrounds.
- Upload images from your computer to overlay on selected backgrounds.
- Automatic background removal for uploaded images.
- Options to send generated images via email, download them, or generate QR codes.
- Intuitive and user-friendly interface.

## Technologies Used:

- Python
- Flask
- Pillow (Python Imaging Library)
- rembg (Background Removal Tool)
- SQLite (Database Management)
- Werkzeug (WSGI Utility Library)
- SMTP (Email Sending)
- SSL (Secure Sockets Layer)
- email.mime (MIME Email Formatting)
- threading (Multithreading)
- pywhatkit (WhatsApp Automation)

## Usage:

### Installation:

To set up the project, you'll need Python 3.11.x. Start by creating a virtual environment within the project directory.

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate`
```

Then, install the required dependencies:

`$ python3 -m pip install -r requirements.txt`

### Running the Application:

Once the dependencies are installed, execute the Flask app:

```bash
$ export FLASK_APP=app.py
$ flask run`
```

Navigate to the provided address in your browser to access the application.

### Deactivating the Virtual Environment:

To deactivate the virtual environment, simply run:

`$ deactivate`

## Contributing:

Contributions to PicBlend are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -am 'Add some amazing feature'`).
4. Push your branch to your fork (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## Starting the Development Server:

To start the development server, use:

```
$ flask run
$ flask --debug run  # (to start it in debug mode)
```

**IMPORTANT:** Run `$ sudo xhost +` before running the server first to allow access to the screen with pywhatkit.
