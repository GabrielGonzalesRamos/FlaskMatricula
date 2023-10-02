from parameterized import parameterized
from test.unit.base_test import BaseTest
import json

class CursoTest(BaseTest):
    @parameterized.expand([
        ('CURSO DE PRUEBA', '2023-09-08', '2023-09-07', 'La fecha final del curso debe de ser mayor que la fecha de inicio'),
        ('CURSO DE PRUEBA', '2023-01-01', '2023-01-02', 'Curso registrado'),
        ('CURSO DE PRUEBA', '2023-01-01', '2023-01-02', 'Curso registrado previamente')
    ])
    def test_post_curso(self, nombre, fecha_inicio, fecha_fin, message):
        data = json.dumps(
            {
                'nombre': nombre,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
        )
        request = self.app().post('/cursos', data = data, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)
    
    @parameterized.expand([
       ('CURSO DE PRUEBA', '2023-09-08', '2023-09-07',1, 'La fecha final del curso debe de ser mayor que la fecha de inicio'),
       ('CURSO DE PRUEBA EDITADO', '2023-01-01', '2023-01-02',1, 'Curso actualizado correctamente'),
       ('CURSO DE PRUEBA EDITADO', '2023-01-01', '2023-01-02',100, 'Curso no registrado')
    ])
    def test_put_curso(self, nombre, fecha_inicio, fecha_fin, id, message):
        data = json.dumps(
            {
                'nombre': nombre,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
            }
        )
        request = self.app().put('/curso/{}'.format(id), data = data, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)