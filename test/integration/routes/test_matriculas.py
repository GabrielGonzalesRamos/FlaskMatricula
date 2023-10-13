from test.unit.base_test import BaseTest
from parameterized import parameterized
from test.helper import create_alumno, create_curso, create_matricula

class MatriculasTest(BaseTest):

    @parameterized.expand([
        (1, 1, 'se ha matriculado exitosamente al curso'),
        (1, 2, 'se ha matriculado exitosamente al curso'),
        (1, 3, 'se ha matriculado exitosamente al curso'),
        (1, 4, 'se ha matriculado exitosamente al curso'),
        (1, 5, 'se ha matriculado exitosamente al curso'),
        (1, 6, 'ha superado el límite máximo de 5 cursos permitidos'),
        (10001, 100, 'Revisar si el id_alumno o id_curso es váido')        
    ])
    def test_create_matricula(self, id_alumno, id_curso, expected):
        create_alumno(self.app)
        create_curso(self.app)
        request_matricula = create_matricula(self.app, id_alumno, id_curso)

        self.assertRegex(request_matricula, r'{}'.format(expected))