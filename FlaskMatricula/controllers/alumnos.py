from flask_restful import Resource
from models.alumno import AlumnoModel
from uuid import uuid4
from serializers.serializerAlumnos import serializerAlumnos, serializerBusqueda
import copy

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


    

        


            

