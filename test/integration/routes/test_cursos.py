from test.unit.base_test import BaseTest
import json

class CursoTest(BaseTest):
    def test_1_create_curso_error_fecha(self):
        request = self.app().post('/cursos', data=json.dumps(
            {
                'nombre': 'CURSO DE PRUEBA',
                'fecha_inicio': '2023-09-08',
                'fecha_fin': '2023-09-07'
            }),
            headers={'Content-Type': 'application/json'}
            )
        self.assertDictEqual(
            {
                'success': False,
                'content': 'None',
                'message': 'La fecha final del curso debe de ser mayor que la fecha de inicio'
            }, 
            json.loads(request.data)
        )