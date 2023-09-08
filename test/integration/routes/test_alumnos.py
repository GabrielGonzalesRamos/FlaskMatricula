from test.unit.base_test import BaseTest
import json

class AlumnoTest(BaseTest):
    def test_1_create_alumno_error_dni(self):
        request = self.app().post('/alumnos', data=json.dumps(
            {
                'dni': '2557819',
                'nombre': 'Walter Emiliano', 
                'apellido': 'Gonzales Inga', 
                'direccion': 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 
                "pais": "Peru",
                'fecha_nacimiento': '1970-11-01', 
            }), 
            headers={'Content-Type': 'application/json'}
            )
        self.assertDictEqual(
            {
                'success': False, 
                'content': None, 
                'message': 'DNI debe de ser una cadena númerica de 8 dígitos'
            },
            json.loads(request.data)
            )

    def test_2_create_alumno(self):
        request = self.app().post('/alumnos', data = json.dumps(
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
        self.assertEqual(request.status_code, 201)
    
    def test_3_create_alumno_duplicated_error(self):
        request = self.app().post('/alumnos', data = json.dumps(
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
        self.assertDictEqual(
            {
                'success': False, 
                'content': None, 
                'message': 'Alumno registrado previamente'
            },
            json.loads(request.data)
            )
        self.assertEqual(request.status_code, 404)
    
    def test_4_get_query_params_alumnos(self):
        request = self.app().get('/busqueda_alumnos', query_string={"dni": "25578190"})
        expected = {
            'dni': '25578190',
            'nombre': 'Walter Emiliano', 
            'apellido': 'Gonzales Inga', 
            'direccion': 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 
            'pais': 'Peru', 
            'fecha_nacimiento': '1970-11-01', 
            'cursos': []
            }
        self.assertDictEqual(
            {
                i: json.loads(request.data).get('content')[0].get(i)
                for i in ['dni', 'nombre', 'apellido', 'direccion', 'pais', 'fecha_nacimiento', 'cursos']
            },
            expected
            )

    def test_5_put_alumno(self):
        request_get = self.app().get('/alumnos')
        request_id = json.loads(request_get.data.decode('utf-8')).get('content')[0].get('id')
        request = self.app().put('/alumno/{}'.format(request_id), data = json.dumps(
            {
                'dni': '25578190',
                'nombre': 'Walter Emiliano', 
                'apellido': 'Gonzales Inga', 
                'direccion': 'Jr. Guisse 587 Callao, 07021', 
                "pais": "Peru",
                'fecha_nacimiento': '1970-11-01', 
            }),
            headers={'Content-Type': 'application/json'}
            )
        self.assertEqual(json.loads(request.data).get('message'), 'Alumno actualizado correctamente')

    def test_6_delete_alumno(self):
        request_get = self.app().get('/alumnos')
        request_id = json.loads(request_get.data.decode('utf-8')).get('content')[0].get('id')
        request_delete = self.app().delete('/alumno/{}'.format(request_id))
        self.assertEqual(json.loads(request_delete.data).get('success'), True)

