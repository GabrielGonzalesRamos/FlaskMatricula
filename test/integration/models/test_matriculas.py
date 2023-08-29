from models.alumno_curso import AlumnoCursoModel
from models.alumno import AlumnoModel
from models.curso import CursoModel
from test.unit.base_test import BaseTest
from uuid import uuid4
from datetime import datetime

class MatriculaTest(BaseTest):
    def test_alumnoCursoModel(self):
        with self.app_context:
            alumno = AlumnoModel(
                matricula = uuid4(),
                nombre = 'Jose Gabriel',
                apellido = 'Gonzales Ramos',
                direccion = 'Freire 2197 Piso 6 Camarones, Región de Arica y Parinacota, 1664830',
                pais = 'Peru',
                fecha_nacimiento = datetime.strptime('1999-02-25',"%Y-%m-%d")
                )
            curso = CursoModel(
                nombre = 'CURSO DE PRUEBA',
                fecha_inicio = datetime.strptime('2023-01-01',"%Y-%m-%d"),
                fecha_fin = datetime.strptime('2023-01-02',"%Y-%m-%d")
                )
            alumno.save()
            curso.save()
            matricula = AlumnoCursoModel(
                alumno = 1,
                curso = 1
            )
            matricula.save()
            self.assertEqual('{} {}'.format(matricula.registroAlumno.alumnoNombre, matricula.registroAlumno.alumnoApellido), 'Jose Gabriel Gonzales Ramos')
            self.assertEqual(matricula.registroCurso.query.first().cursoNombre, 'CURSO DE PRUEBA')
            expected = {
                'nombre': 'Jose Gabriel', 
                'apellido': 'Gonzales Ramos', 
                'direccion': 'Freire 2197 Piso 6 Camarones, Región de Arica y Parinacota, 1664830', 
                'pais': 'Peru', 
                'fecha_nacimiento': '1999-02-25', 
                'cursos': ['CURSO DE PRUEBA']
                }
            result = {
                i: matricula.registroAlumno.join_json().get(i) 
                for i in ['nombre', 'apellido', 'direccion', 'pais', 'fecha_nacimiento', 'cursos']
                }
            self.assertDictEqual(result, expected)
            matricula.delete()
            curso.delete()
            alumno.delete()

