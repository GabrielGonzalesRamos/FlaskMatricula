from flask_restful import Resource, reqparse
from models.alumno import AlumnoModel
from uuid import uuid4
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
class AlumnoController(Resource):
    def post(self):
        data = serializerAlumnos.parse_args()
        nuevoAlumno = AlumnoModel(nombre=data.get('nombre'), apellido=data.get('apellido'), direccion=data.get('direccion'), pais=data.get('pais'), fecha_nacimiento=data.get('fecha_nacimiento'), matricula=uuid4())
        nuevoAlumno.save()
        return {
            'success': True,
            'content': nuevoAlumno.json(),
            'message': 'Alumno registrado',
        }, 201

