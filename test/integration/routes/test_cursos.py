from parameterized import parameterized
from test.unit.base_test import BaseTest
from test.helper import data_curso, data_curso_error
import json

class CursoTest(BaseTest):
    
    curso_data = data_curso()

    @parameterized.expand([
        (curso_data, 'Curso registrado'),
        (curso_data, 'Curso registrado previamente'),
        (data_curso_error(), 'La fecha final del curso debe de ser mayor que la fecha de inicio')
    ])
    def test_post_curso(self, curso, message):
        request = self.app().post('/cursos', data = curso, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)
    
    @parameterized.expand([
        (data_curso_error(), 1, 'La fecha final del curso debe de ser mayor que la fecha de inicio'),
        (curso_data, 1, 'Curso actualizado correctamente'),
        (curso_data, 2, 'Curso no registrado'),
    ])
    def test_put_curso(self, curso, id, message):
        request = self.app().put('/curso/{}'.format(id), data = curso, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)