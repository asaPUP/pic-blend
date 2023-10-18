<h1>Bienvenido a SISTEMIN jiji</h1>
Proyecto para la materia de Ingenieria de Software.

## Instalación del proyecto

Para la instalación se necesita Python 3.11.x. Primeramente se crea una 
máquina virtual dentro del directorio raíz del proyecto.

UNIX:
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```

WINDOWS:
```
> virtualenv venv
> .\venv\Scripts\activate
```

Luego, se instalan las dependencias usando pip.

UNIX:
```
$ (venv) python3 -m pip install -r requirements.txt
```

WINDOWS:
```
(venv) > pip install -r requirements.txt
```

## Ejecución del proyecto

Y finalmente, ejecutamos la app de Flask.

UNIX:
```
$ (venv) export FLASK_APP=app.py
$ (venv) flask run
```

WINDOWS:
```
(venv) > flask run
```

Ingresa a la dirección que te indica la terminal para ver la aplicación.

## Desactivar el entorno virtual

Para desactivar el entorno virtual, ejecuta el siguiente comando:

UNIX:
```
$ (venv) deactivate
```

WINDOWS:
```
(venv) > deactivate
```