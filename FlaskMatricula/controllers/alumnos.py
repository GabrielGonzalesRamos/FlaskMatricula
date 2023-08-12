from flask_restful import Resource, reqparse
from models.alumno import AlumnoModel
from config.conexion_bd import base_de_datos
from uuid import uuid4
from datetime import datetime
import copy

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


class AlumnosController(Resource):
    def get(self):
        alumnos = AlumnoModel.query.all()
        lista_alumnos = []
        for i in alumnos:
            lista_alumnos.append(i.json())
        return {
            'success': True,
            'content': lista_alumnos,
            'message': None
        }, 200
        
    def post(self):
        data = serializerAlumnos.parse_args()
        nuevoAlumno = AlumnoModel(nombre=data.get('nombre'), apellido=data.get('apellido'), direccion=data.get('direccion'), pais=data.get('pais'), fecha_nacimiento=data.get('fecha_nacimiento'), matricula=uuid4())
        try:
            nuevoAlumno.save()
            return {
                'success': True,
                'content': nuevoAlumno.json(),
                'message': 'Alumno registrado',
                }, 201
        except Exception as E:
            return {
                'success': False,
                'content': None,
                'message': f'{E}'
                }, 203

class AlumnoController(Resource):
    def get(self, id):
        alumno = AlumnoModel.query.filter_by(alumnoId=id).first()
        return (
            {
            'success': True,
            'content': alumno.json(),
            'message': 'Alumno {} {} matriculado'.format(AlumnoModel.query.filter_by(alumnoId=id).first().alumnoNombre, AlumnoModel.query.filter_by(alumnoId=id).first().alumnoApellido)
            }, 200) if alumno else (
            {
                'success': False,
                'content': None,
                'message': 'Alumno no matriculado'
            }, 404)

    def put(self, id):
        alumno = AlumnoModel.query.filter_by(alumnoId=id).first()
        if alumno:
            alumno_viejo = copy.deepcopy(alumno)
            data = serializerAlumnos.parse_args()
            alumno.alumnoNombre = data.get('nombre')
            alumno.alumnoApellido = data.get('apellido')
            alumno.alumnoDireccion = data.get('direccion')
            alumno.alumnoPais = data.get('pais')
            alumno.alumnoFechaNacimiento = data.get('fecha_nacimiento')
            alumno.save()
            return {
                'success': True,
                'content': [alumno_viejo.json(), alumno.json()],
                'message': 'Alumno actualizado correctamente'
                }, 201
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Alumno no matriculado'
            }, 404

    def delete(self, id):
        alumno = AlumnoModel.query.filter_by(alumnoId=id)
        print(alumno)
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # Se usa session seguido del método query debido a que SQLALCHEMY lo admite
        # En FLASKSQLALCHEMY solo es necesario el Model seguido del método query
        # base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id).first().__dict__
        if alumno.first():
            alumno_viejo = copy.deepcopy(alumno.first())
            alumno.delete()
            base_de_datos.session.commit()
            return {
                'success': True,
                'content': [alumno_viejo.json()],
                'message': 'Alumno {} {} eliminado'.format(alumno_viejo.alumnoNombre, alumno_viejo.alumnoApellido)
            }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Alumno eliminado o no existe'
            }, 404

        


            

