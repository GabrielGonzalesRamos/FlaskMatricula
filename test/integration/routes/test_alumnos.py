from parameterized import parameterized
from test.unit.base_test import BaseTest
from unittest.mock import Mock
import json

class AlumnoTest(BaseTest):

    @parameterized.expand([
        ('2557819', 'Walter Emiliano', 'Gonzales Inga', 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 'Peru', '1970-11-01', 'DNI debe de ser una cadena númerica de 8 dígitos'),
        ('25578190', 'Walter Emiliano', 'Gonzales Inga', 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 'Peru', '1970-11-01', 'Alumno registrado'),
        ('25578190', 'Walter Emiliano', 'Gonzales Inga', 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 'Peru', '1970-11-01', 'Alumno registrado previamente')
    ])    
    def test_post_alumno(self, dni, nombre, apellido, direccion, pais, fecha_nacimiento, message):
        data = json.dumps(
            {
                'dni': dni,
                'nombre': nombre, 
                'apellido': apellido,
                'direccion': direccion,
                "pais": pais,
                'fecha_nacimiento': fecha_nacimiento,
            })
        
        request = self.app().post('/alumnos', data = data, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)

    @parameterized.expand([
        ('2557819', 'Walter Emiliano', 'Gonzales Inga', 'Jr. Guisse 587 Callao, 07021', 'Peru', '1970-11-01',1, 'DNI debe de ser una cadena númerica de 8 dígitos'),
        ('25578190', 'Walter Emiliano', 'Gonzales Inga', 'Jr. Guisse 587 Callao, 07021', 'Peru', '1970-11-01',1, 'Alumno actualizado correctamente'),
        ('25578190', 'Walter Emiliano', 'Gonzales Inga', 'Jr. Guisse 587 Callao, 07021', 'Peru', '1970-11-01',100, 'Alumno no matriculado')
        ]) 
    def test_put_alumno(self, dni, nombre, apellido, direccion, pais, fecha_nacimiento, id, message):
        data = json.dumps(
            {
                'dni': dni,
                'nombre': nombre, 
                'apellido': apellido, 
                'direccion': direccion, 
                "pais": pais,
                'fecha_nacimiento': fecha_nacimiento, 
            })
        request = self.app().put('/alumno/{}'.format(id), data = data, headers={'Content-Type': 'application/json'})
        self.assertEqual(json.loads(request.data).get('message'), message)
