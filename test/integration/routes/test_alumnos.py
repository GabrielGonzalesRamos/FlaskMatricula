from test.unit.base_test import BaseTest
import json

class AlumnoTest(BaseTest):
    def test_create_alumno(self):
        with self.app() as client:
            request = client.post('/alumnos', data = json.dumps({
                "nombre": "Jose Gabriel",
                "apellido": "Gonzales Ramos",
                "direccion": "Freire 2197 Piso 6 Camarones, Región de Arica y Parinacota, 1664830",
                "pais": "Peru",
                "fecha_nacimiento": "1999-02-25"
                }), headers={'Content-Type': 'application/json'})
            self.assertEqual(request.status_code, 201)
