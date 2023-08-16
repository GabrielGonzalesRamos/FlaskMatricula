from flask_restful import Resource
from models.alumno import AlumnoModel
from uuid import uuid4
from serializers.serializerAlumnos import serializerAlumnos, serializerBusqueda
from config.conexion_bd import base_de_datos
import copy

class AlumnosController(Resource):

    def get(self):
        alumnos = base_de_datos.session.query(AlumnoModel).all()
        if alumnos:
            return {
                'success': True,
                'message': 'Cantidad total de alumnos {}'.format(base_de_datos.session.query(AlumnoModel).count()),
                'content': [i.json() for i in alumnos]
                }, 200
        else:
            return {
                'success': False,
                'message': 'No se encontraron alumnos',
                'content': None
            }
        
    def post(self):
        data = serializerAlumnos.parse_args()
        nuevoAlumno = AlumnoModel(\
            nombre=data.get('nombre'), \
            apellido=data.get('apellido'), \
            direccion=data.get('direccion'), \
            pais=data.get('pais'), \
            fecha_nacimiento=data.get('fecha_nacimiento'), \
            matricula=uuid4())
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
        alumno = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id).first()
        if alumno:
            return {
                'success': True,
                'content': alumno.json(),
                'message': 'Alumno {} {} matriculado'.format(alumno.alumnoNombre, alumno.alumnoApellido)
                }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Alumno no matriculado'
                }, 404

    def put(self, id):
        alumno = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id).first()
        if alumno:
            data = serializerAlumnos.parse_args()
            alumno_viejo = copy.deepcopy(alumno)
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
        alumno = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id)
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
            filters.append(AlumnoModel.alumnoNombre.like('%{}%'.format(data.get('nombre'))))
        if data.get('apellido'):
            filters.append(AlumnoModel.alumnoApellido.like('%{}%'.format(data.get('apellido'))))
        if data.get('pais'):
            filters.append(AlumnoModel.alumnoPais.like('%{}%'.format(data.get('pais'))))
            
        resultado = base_de_datos.session.query(AlumnoModel).filter(*filters).all()

        if bool(filters):
            return {
                'success': True,
                'content': [i.json() for i in resultado],
                'message': 'Se encontraron {} coincidencias'.format(base_de_datos.session.query(AlumnoModel).filter(*filters).count())
            }
        else: 
            return {
                'success': False,
                'content': None,
                'message': 'Filtro vacío'
            }






