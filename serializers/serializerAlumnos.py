from flask_restful import Resource, reqparse
from datetime import datetime

serializerAlumnos = reqparse.RequestParser(bundle_errors=True)

serializerAlumnos.add_argument(
    'nombre',
    type=str,
    required=True,
    help='Nombre del alumno obligatorio',
    location='json'
)
serializerAlumnos.add_argument(
    'apellido',
    type=str,
    required=True,
    help='Apellido del alumno obligatorio',
    location='json'
)
serializerAlumnos.add_argument(
    'direccion',
    type=str,
    required=True,
    help='Dirección del alumno obligatorio',
    location='json'
)
serializerAlumnos.add_argument(
    'pais',
    type=str,
    required=True,
    choices=('Mexico', 'Chile', 'Colombia', 'Argentina', 'Peru'),
    help='Pais del alumno obligatorio o pais válido',
    location='json'
)
serializerAlumnos.add_argument(
    'fecha_nacimiento',
    type=lambda x: datetime.strptime(x,"%Y-%m-%d"),
    required=True,
    help='Fecha de nacimiento del alumno obligatorio',
    location='json'
)

serializerBusqueda = reqparse.RequestParser(bundle_errors=True)

serializerBusqueda.add_argument(
    'nombre',
    type=str,
    location='args',
    required=False
)
serializerBusqueda.add_argument(
    'apellido',
    type=str,
    location='args',
    required=False
)
serializerBusqueda.add_argument(
    'pais',
    type=str,
    location='args',
    required=False,
    choices=('Mexico', 'Chile', 'Colombia', 'Argentina', 'Peru'),
    help='Pais invalido'
)