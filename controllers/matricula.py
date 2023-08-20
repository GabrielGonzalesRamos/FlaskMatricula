from flask_restful import Resource
from config.conexion_bd import base_de_datos
from models.alumno_curso import AlumnoCursoModel
from models.alumno import AlumnoModel
from models.curso import CursoModel
from serializers.serializerMatricula import serializerMatricula
import copy

class MatriculaController(Resource):

    def post(self):
        data = serializerMatricula.parse_args()
        if len(base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first().alumnoRegistrados) >= 5:
            return {
                'success': False,
                'content': None,
                'message': f"El alumno {base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first().alumnoNombre} {base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first().alumnoApellido} ha superado el límite máximo de 5 cursos permitidos"
            }, 203
        if base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first() and base_de_datos.session.query(CursoModel).filter_by(cursoId=data.get('id_curso')).first():
            try:
                nuevaMatricula = AlumnoCursoModel(alumno=data.get('id_alumno'), curso=data.get('id_curso'))
                nuevaMatricula.save()
                return {
                    'success': True,
                    'content': nuevaMatricula.registroAlumno.join_json(),
                    'message': f'El alumno {nuevaMatricula.registroAlumno.alumnoNombre} {nuevaMatricula.registroAlumno.alumnoApellido} se ha matriculado exitosamente al curso {nuevaMatricula.registroCurso.cursoNombre}'
                }, 201
            except Exception as E:
                base_de_datos.session.rollback()
                alumnoMatricula = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first()
                cursoMatricula = base_de_datos.session.query(AlumnoCursoModel).filter_by(acIdAlumno=data.get('id_alumno'))
                return {
                    'success': False,
                    'content': [i.registroCurso.cursoNombre for i in cursoMatricula.all()],
                    'message': f'El alumno {alumnoMatricula.alumnoNombre} {alumnoMatricula.alumnoApellido} ya se encuentra matriculado en el curso'
                }, 203
    
    def delete(self):
        data = serializerMatricula.parse_args()
        alumnoMatricula = base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=data.get('id_alumno')).first()
        cursoMatricula = base_de_datos.session.query(CursoModel).filter_by(cursoId=data.get('id_curso')).first()
        alumnoCursoMatricula = base_de_datos.session.query(AlumnoCursoModel).filter_by(acIdAlumno=data.get('id_alumno'), acIdCurso=data.get('id_curso')).first()
        if alumnoMatricula and cursoMatricula and alumnoCursoMatricula:
            copy_alumnoMatricula = copy.deepcopy(alumnoMatricula.join_json())
            alumnoCursoMatricula.delete()
            return {
                'success': True,
                'content': [
                    copy_alumnoMatricula,
                    alumnoMatricula.join_json()
                ],
                'message': 'Se ha retirado al alumno {} del curso {}'.format(alumnoMatricula.alumnoApellido, cursoMatricula.cursoNombre)
            }
            


        
