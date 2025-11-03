from flask_restful import Resource
from models.alumno import AlumnoModel
from serializers.serializerAlumnos import serializerAlumnos, serializerBusqueda
from config.conexion_bd import base_de_datos
from elasticapm import get_client
import copy

class AlumnosController(Resource):
    def get(self):
        alumnos = base_de_datos.session.query(AlumnoModel).all()
        if alumnos:
            alumnos_cursos = [i.json() for i in alumnos]
            cantidad_cursos = [len(i.alumnoRegistrados) for i in alumnos]
            get_client().capture()
            return {
                'success': True,
                'message': 'Cantidad total de alumnos {}'.format(base_de_datos.session.query(AlumnoModel).count()),
                'content': sorted([{**j, 'cantidad_cursos_matriculados': i} for i, j in zip(cantidad_cursos, alumnos_cursos)], key=lambda x: x['cantidad_cursos_matriculados'], reverse=True)
                }, 200
        else:
            get_client().capture_exception()
            return {
                'success': False,
                'message': 'No se encontraron alumnos',
                'content': None
            }, 404
        
        
    def post(self):
        data = serializerAlumnos.parse_args()
        nuevoAlumno = AlumnoModel(\
            dni=data.get('dni'), \
            nombre=data.get('nombre'), \
            apellido=data.get('apellido'), \
            direccion=data.get('direccion'), \
            pais=data.get('pais'), \
            fecha_nacimiento=data.get('fecha_nacimiento'), \
            )
        if not data.get('dni').isdigit() or len(data.get('dni')) != 8:
            return {
                'success': False,
                'content': None,
                'message': 'DNI debe de ser una cadena númerica de 8 dígitos'
            }
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
                'message': 'Alumno registrado previamente'
                }, 404

class AlumnoController(Resource):

    def get(self, id):
        alumno = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id).first()
        if alumno:
            return {
                'success': True,
                'content': alumno.join_json_id(id),
                'message': 'Alumno {} {} matriculado'.format(alumno.alumnoNombre, alumno.alumnoApellido)
                }, 200
        else:
            get_client().capture_exception()
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
            alumno.alumnoDNI = data.get('dni')
            alumno.alumnoNombre = data.get('nombre')
            alumno.alumnoApellido = data.get('apellido')
            alumno.alumnoDireccion = data.get('direccion')
            alumno.alumnoPais = data.get('pais')
            alumno.alumnoFechaNacimiento = data.get('fecha_nacimiento')
            if not data.get('dni').isdigit() or len(data.get('dni')) != 8:
                return {
                    'success': False,
                    'content': None,
                    'message': 'DNI debe de ser una cadena númerica de 8 dígitos'
                }, 404
            alumno.save()
            return {
                'success': True,
                'content': [alumno_viejo.join_json_id(id), alumno.join_json_id(id)],
                'message': 'Alumno actualizado correctamente'
                }, 200
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
        if data.get('dni'):
            filters.append(AlumnoModel.alumnoDNI.like('%{}%'.format(data.get('dni'))))
        resultado = base_de_datos.session.query(AlumnoModel).filter(*filters).all()

        if bool(filters):      
            return {
                'success': True,
                'content': [i.join_json() for i in resultado],
                'message': 'Se encontró 1 coincidencia' if base_de_datos.session.query(AlumnoModel).filter(*filters).count() == 1 else 'Se encontraron {} coincidencias'.format(base_de_datos.session.query(AlumnoModel).filter(*filters).count())
            }, 200
        else: 
            return {
                'success': False,
                'content': None,
                'message': 'Sin coincidencias'
            }, 404






