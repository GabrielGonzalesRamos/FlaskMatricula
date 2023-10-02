from test.unit.base_test import BaseTest
import json

class MatriculasTest(BaseTest):
    def test_1_create_error_matricula_without_curso(self):
        request_alumno = self.app().post('/alumnos', data=json.dumps(
            {
                'dni': '25578190',
                'nombre': 'Walter Emiliano', 
                'apellido': 'Gonzales Inga', 
                'direccion': 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 
                "pais": "Peru",
                'fecha_nacimiento': '1970-11-01', 
            }), 
            headers={'Content-Type': 'application/json'}
            )
        request_get_alumno = self.app().get('/busqueda_alumnos', query_string={"dni": "25578190"})
        id_alumno = json.loads(request_get_alumno.data).get('content')[0].get('id')
        request_create_error_matricula = self.app().post('/matricula', data = json.dumps(
            {
                "id_alumno": id_alumno,
                "id_curso": "1"
            }),
            headers={'Content-Type': 'application/json'}
            )
        self.assertDictEqual(
            {
                'success': False,
                'content': None,
                'message': 'Revisar si el id_alumno o id_curso es váido'
            },
            json.loads(request_create_error_matricula.data)
        )
        request_delete_alumno = self.app().delete('alumno/{}'.format(id_alumno))
        self.assertEqual(request_delete_alumno.status_code, 200)
        
    def test_2_create_error_matricula_without_alumno(self):
        request_curso = self.app().post('/cursos', data=json.dumps(
            {
                "nombre": "CURSO DE PRUEBA",
                "fecha_inicio": "2023-10-01",
                "fecha_fin": "2023-10-02"
            }),
            headers={'Content-Type': 'application/json'}
            )
        request_get_curso = self.app().get('/busqueda_cursos', query_string={"nombre": "CURSO DE PRUEBA"})
        id_curso = json.loads(request_get_curso.data).get('content')[0].get('id')
        request_create_error_matricula = self.app().post('/matricula', data = json.dumps(
            {
                "id_alumno": "1",
                "id_curso": id_curso
            }),
            headers={'Content-Type': 'application/json'}
            )
        self.assertDictEqual(
            {
                'success': False,
                'content': None,
                'message': 'Revisar si el id_alumno o id_curso es váido'
            },
            json.loads(request_create_error_matricula.data)
        )