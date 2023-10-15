from models.alumno_curso import AlumnoCursoModel
from models.alumno import AlumnoModel
from models.curso import CursoModel
from test.unit.base_test import BaseTest
from test.helper import data_alumno, data_curso, data_matricula
import json

class MatriculaTest(BaseTest):
    def test_alumnoCursoModel(self):
        alumno_data = json.loads(data_alumno()).values()
        curso_data = json.loads(data_curso()).values()
        matricula_data = json.loads(data_matricula(1,1)).values()
        with self.app_context():
            alumno = AlumnoModel(*alumno_data)
            curso = CursoModel(*curso_data)
            matricula = AlumnoCursoModel(*matricula_data)
            alumno.save()
            curso.save()
            matricula.save()
            self.assertTrue(AlumnoCursoModel.query.all())
            matricula.delete()
            self.assertFalse(AlumnoCursoModel.query.all())
            



