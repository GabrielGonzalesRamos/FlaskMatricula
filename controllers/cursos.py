from sqlalchemy import extract
from flask_restful import Resource
from config.conexion_bd import base_de_datos
from models.curso import CursoModel
from serializers.serializerCursos import serializerCursos, serializerBusqueda
from datetime import datetime
import copy


class CursosController(Resource):

    def get(self):
        cursos = base_de_datos.session.query(CursoModel).all()
        if cursos:
            return {
                'success': True,
                'message': 'Cantidad total de cursos {}'.format(base_de_datos.session.query(CursoModel).count()),
                'content': [i.json() for i in cursos]
            }, 201
    
    def post(self):
        data = serializerCursos.parse_args()
        if data.get('fecha_fin') < data.get('fecha_inicio'):
            return {
                'success': False,
                'content': 'None',
                'message': 'La fecha final del curso debe de ser mayor que la fecha de inicio'
            }, 203
        nuevoCurso = CursoModel(nombre=data.get('nombre'), fecha_inicio=data.get('fecha_inicio'), fecha_fin=data.get('fecha_fin'))
        try:
            nuevoCurso.save()
            return {
                'success': True,
                'content': nuevoCurso.json(),
                'message': 'Curso registrado'
            }, 201
        except Exception as E:
            return {
                'success': False,
                'content': None,
                'message': f'{E}'
            }, 203

class CursoController(Resource):

    def get(self, id):
        curso = base_de_datos.session.query(CursoModel).filter_by(cursoId=id).first()
        if curso:
            return {
                'success': True,
                'content': curso.json(),
                'message': 'Curso {} registrado'.format(curso.cursoNombre)
            }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Curso no registrado'
            }, 203

    def put(self, id):
        curso = base_de_datos.session.query(CursoModel).filter_by(cursoId=id).first()
        data = serializerCursos.parse_args()
        if curso and data.get('fecha_inicio') > data.get('fecha_fin'):
            return {
                'success': False,
                'content': None,
                'message': 'La fecha final del curso debe de ser mayor que la fecha de inicio'
            }, 203
        if curso:
            curso_viejo = copy.deepcopy(curso)
            curso.cursoNombre = data.get('nombre')
            curso.cursoFechaInicio = data.get('fecha_inicio')
            curso.cursoFechaFin = data.get('fecha_fin')
            curso.save()
            return {
                'success': True,
                'content': [curso_viejo.json(), curso.json()],
                'message': 'Curso actualizado correctamente'
            }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Curso no registrado'
            }, 404

    def delete(self, id):
        curso = base_de_datos.session.query(CursoModel).filter_by(cursoId=id)
        if curso.first():
            curso_viejo = copy.deepcopy(curso.first())
            curso.first().delete()
            return {
                'success': True,
                'content': [curso_viejo.json()],
                'message': 'Curso {} eliminado'.format(curso_viejo.cursoNombre)
            }, 200
        else: 
            return {
                'success': False,
                'content': None,
                'message': 'Curso eliminado no existe'
            }, 404

class BusquedaCursos(Resource):

    def get(self):
        data = serializerBusqueda.parse_args()
        filters = []
        if data.get('nombre'):
            filters.append(CursoModel.cursoNombre.like('%{}%'.format(data.get('nombre'))))
        if data.get('mes_inicio'):
            filters.append(extract('month', CursoModel.cursoFechaInicio) == data.get('mes_inicio'))
        
        resultado = base_de_datos.session.query(CursoModel).filter(*filters).all()
        
        if bool(resultado):
            return {
                'success': True,
                'content': [i.json() for i in resultado],
                'message': 'Se encontraron {} coincidencias'.format(base_de_datos.session.query(CursoModel).filter(*filters).count())
            }, 200
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Sin coincidencias'
            }, 404


