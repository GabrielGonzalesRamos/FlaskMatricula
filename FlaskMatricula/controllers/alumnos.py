from flask_restful import Resource
from models.alumno import AlumnoModel
from uuid import uuid4
from serializers.serializerAlumnos import serializerAlumnos, serializerBusqueda
from config.conexion_bd import base_de_datos
import copy

class AlumnosController(Resource):

    def get(self):
        alumnos = AlumnoModel.query.all()
        lista_alumnos = []
        for i in alumnos:
            lista_alumnos.append(i.json())
        return {
            'success': True,
            'message': 'Cantidad total de alumnos {}'.format(AlumnoModel.query.count()),
            'content': lista_alumnos
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
        if alumno.first():
            alumno_viejo = copy.deepcopy(alumno.first())
            alumno.first().delete()
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

class BusquedaAlumnos(Resource):
    def get(self):
        data = serializerBusqueda.parse_args()

        filters = []

        if data.get('nombre'):
            filters.append(AlumnoModel.alumnoNombre == data.get('nombre'))
        if data.get('apellido'):
            filters.append(AlumnoModel.alumnoApellido == data.get('apellido'))
        if data.get('pais'):
            filters.append(AlumnoModel.alumnoPais == data.get('pais'))

        resultado = AlumnoModel.query.filter(*filters).all()

        if bool(resultado):
            return {
                'success': True,
                'content': [i.json() for i in resultado],
                'message': 'Se encontraron {} coincidencias'.format(AlumnoModel.query.filter(*filters).count())
            }
        else: 
            return {
                'success': False,
                'content': None,
                'message': 'Se encontraron 0 coincidencias'
            }






