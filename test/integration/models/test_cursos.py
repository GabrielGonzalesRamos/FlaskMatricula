from models.curso import CursoModel
from test.unit.base_test import BaseTest
from test.helper import data_curso
import json

class CursoTest(BaseTest):
    def test_cursoModel(self):
        data = json.loads(data_curso()).values()
        with self.app_context():
            curso = CursoModel(*data)
            curso.save()
            self.assertTrue(CursoModel.query.all())
            curso.delete()
            self.assertFalse(CursoModel.query.all())