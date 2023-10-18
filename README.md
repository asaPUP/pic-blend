<h1>Bienvenido a SISTEMIN jiji</h1>
Proyecto para la materia de Ingenieria de Software.

## Instalación
Para la instalación se necesita Python 3.11.x. Primeramente se crea una 
máquina virtual dentro del directorio raíz del proyecto.
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```
Luego, se instalan las dependencias usando pip.
```
$ (venv) python3 -m pip install -r requirements.txt
```
Y finalmente, ejecutamos la app de Flask.
```
$ (venv) export FLASK_APP=main.py
$ (venv) flask run
```
