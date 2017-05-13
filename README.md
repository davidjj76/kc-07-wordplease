# Wordplease

Ejercicio de la práctica de backend avanzado

## Índice

* [Instalación](#toc_2)
* [Arranque de la app](#toc_3)

## Instalación

Hay un script de instalación ```install.sh``` que: 

1. Crea el entorno virtual en env/
2. Instala las dependencias en el mismo con *pip install* (*necesario python 3.5*)
3. Crea un usuario con privilegios de administrador *(password de todos los usuarios: **seguridad**)*
4. Carga un juego deenlace datos de ejemplo (unas categorías y un blog y un post por cada usuario)

Para ejecutar el instalador, sitúate en la carpeta del proyecto desde el terminal y ejecuta:

```
$ ./install.sh
```

## Arranque de la app

### Servidor web

Para arrancar el servidor, hay que *activar el entorno virtual* y luego *arrancar el servidor* de desarrollo de Django.

Desde la carpeta del proyecto y en el terminal, ejecuta:

```
$ source env/bin/activate
(env)$ python manage.py runserver
```

### Celery (servicio de procesamiento en background)

Celery se encarga de ejecutar tareas pesada en background:

1. Procesamiento de las imágenes subidas a la plataforma.
2. Envío de notificaciones por email a usuarios replicados y mencionados en los posts.

Para arrancar Celery, hay que *activar el entorno virtual* y luego *arrancar el Celery*.

Desde la carpeta del proyecto y en el terminal, ejecuta:

```
$ source env/bin/activate
(env)$ celery -A wordplease worker -l info
```
El message broker utilizado es *rabbitmq*, por lo que tendrás que tener un servidor del mismo corriendo en la máquina.

***
**Nota:** el sitio está disponible en español e inglés, para cambiar rápidamente el idioma del usuario yo utilizo esta extensión de chrome:

[Quick Language Switcher](https://chrome.google.com/webstore/detail/quick-language-switcher/pmjbhfmaphnpbehdanbjphdcniaelfie?utm_source=chrome-app-launcher-info-dialog)


***
#### TODO ####

1. Implementar las API para gestionar usuarios y posts, aunque la existencia de un API no cambiaría la solución a las tareas de background, ya que estas se gestionan directamente desde el modelo.

2. Implementar tests.

3. Pasar a una arquirectura de microservicios.
