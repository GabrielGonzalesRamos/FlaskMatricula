from flask_restful import Resource
from config.conexion_bd import base_de_datos
from models.curso import CursoModel
from models.alumno import AlumnoModel
from models.alumno_curso import AlumnoCursoModel
from datetime import datetime
import copy


class MatriculasController(Resource):

    def get(self):
        data = base_de_datos.session.query(CursoModel).filter_by(cursoRegistrados=11).all()