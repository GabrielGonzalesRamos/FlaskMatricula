from models.curso import CursoModel
from test.unit.base_test import BaseTest
from datetime import datetime

class CursoTest(BaseTest):
    def test_cursoModel(self):
        with self.app_context:
            curso = CursoModel(
                nombre = 'CURSO DE PRUEBA',
                fecha_inicio = datetime.strptime('2023-01-01',"%Y-%m-%d"),
                fecha_fin = datetime.strptime('2023-01-02',"%Y-%m-%d")
                )
            self.assertIsNone(CursoModel.query.filter_by(cursoNombre='CURSO DE PRUEBA').first())
            curso.save()
            self.assertIsNotNone(CursoModel.query.filter_by(cursoNombre='CURSO DE PRUEBA').first())
            curso.delete()
            self.assertIsNone(CursoModel.query.filter_by(cursoNombre='CURSO DE PRUEBA').first())