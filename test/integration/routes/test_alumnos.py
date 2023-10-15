from parameterized import parameterized
from test.unit.base_test import BaseTest
from test.helper import data_alumno, data_alumno_error
import json

class AlumnoTest(BaseTest):

    alumno_data = data_alumno()

    @parameterized.expand([
        (alumno_data, 'Alumno registrado'),
        (alumno_data, 'Alumno registrado previamente'),
        (data_alumno_error(), 'DNI debe de ser una cadena númerica de 8 dígitos')
    ])
    def test_post_alumno(self, alumno, message):
        request = self.app().post('/alumnos', data = alumno, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)

    @parameterized.expand([
        (data_alumno_error(), 1, 'DNI debe de ser una cadena númerica de 8 dígitos'),
        (data_alumno(), 1, 'Alumno actualizado correctamente'),
        (data_alumno(), 2, 'Alumno no matriculado')
    ])
    def test_put_alumno(self, alumno, id, message):
        request = self.app().put('/alumno/{}'.format(id), data = alumno, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)