# Repositorio prueba técnica de SMART DATA en Python


### Librerías :
- Django: [Documentación de Django](https://docs.djangoproject.com/)
- Django REST Framework: [Documentación de Django REST Framework](https://www.django-rest-framework.org/)


## Estructura 
## Raiz
```
.
├── suscripciones_api/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
```
## UsuariosApp
```
├── UsuariosApp
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── models.py
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── manage.py
└── requirements.txt
```
## SuscripcionesApp
```
├── SuscripcionesApp
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── models.py
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── manage.py
└── requirements.txt
```



## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. Clona el repositorio:

```bash
git clone https://github.com/cedioza/backned_smart_data.git
```
Crea y activa un entorno virtual:


```
python3 -m venv nombre_del_entorno_virtual
source nombre_del_entorno_virtual/bin/activate
```
Instala las dependencias del proyecto:
```
pip install -r requirements.txt
```

## Paso a Paso

Abre una terminal y navega a la carpeta raíz de tu proyecto.
Crea un nuevo entorno virtual con venv usando el siguiente comando:


```
python3 -m venv venv
```
Activa el entorno Virtual.
```
./venv/Scripts/Activate
```
Instalar con pip:
```
$ pip install -r requirements.txt
```
## Requisito 

Este proyecto tiene los siguientes endpoints:

/usuarios: Este endpoint se utiliza para realizar operaciones relacionadas con usuarios, como la creación, lectura, actualización y eliminación de usuarios. Permite gestionar información como nombres, correos electrónicos y contraseñas de los usuarios.

/servicios: Este endpoint proporciona funcionalidades para administrar servicios. Puedes realizar operaciones como la creación, lectura, actualización y eliminación de servicios. Cada servicio puede tener atributos como nombre, url_api y api_key.

/suscripciones: Este endpoint se utiliza para gestionar las suscripciones de los usuarios a servicios específicos. Permite realizar operaciones como la creación, lectura, actualización y eliminación de suscripciones. Cada suscripción puede contener información como el usuario asociado, el servicio.

Si tienes alguna pregunta o problema, no dudes en crear un issue en el repositorio o contactar al equipo de desarrollo al correo cedioza@gmail.com

## Pruebas coverage 
```
coverage run --source='.' manage.py test ; coverage report --fail-under=80
```



| Name                             | Stmts | Miss | Cover |
|----------------------------------|-------|------|-------|
| SuscripcionesApp\admin.py         | 1     | 0    | 100%  |
| SuscripcionesApp\apps.py          | 4     | 0    | 100%  |
| SuscripcionesApp\models.py        | 16    | 2    | 88%   |
| SuscripcionesApp\serializers.py   | 10    | 0    | 100%  |
| SuscripcionesApp\tests.py         | 63    | 0    | 100%  |
| SuscripcionesApp\views.py         | 80    | 40   | 50%   |
| UsuariosApp\admin.py              | 1     | 0    | 100%  |
| UsuariosApp\apps.py               | 4     | 0    | 100%  |
| UsuariosApp\models.py             | 10    | 1    | 90%   |
| UsuariosApp\serializers.py        | 6     | 0    | 100%  |
| UsuariosApp\tests.py              | 41    | 0    | 100%  |
| UsuariosApp\views.py              | 34    | 12   | 65%   |
|----------------------------------|-------|------|-------|
| TOTAL                            | 270   | 55   | 80%   |

## Swagger

para acceder a documentación en Swagger podemos acceder al siguiente enlace en nuestro proyecto ya arancado 

http://127.0.0.1:8000/swagger/

Adicional tiene una documentacion corta en postman

https://documenter.getpostman.com/view/17377152/2s93m354EM#aa600443-bcce-454e-bac4-9befed7e1486

