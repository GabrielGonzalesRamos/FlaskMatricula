from models.alumno_curso import AlumnoCursoModel
from models.alumno import AlumnoModel
from models.curso import CursoModel
from test.unit.base_test import BaseTest
from datetime import datetime

class MatriculaTest(BaseTest):
    def test_alumnoCursoModel(self):
        with self.app_context:
            alumno = AlumnoModel(
                dni = '25578190',
                nombre = 'Walter Emiliano',
                apellido = 'Gonzales Inga',
                direccion = 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100',
                pais = 'Peru',
                fecha_nacimiento = datetime.strptime('1970-11-01',"%Y-%m-%d")
                )
            curso = CursoModel(
                nombre = 'CURSO DE PRUEBA',
                fecha_inicio = datetime.strptime('2023-01-01',"%Y-%m-%d"),
                fecha_fin = datetime.strptime('2023-01-02',"%Y-%m-%d")
                )
            alumno.save()
            curso.save()
            matricula = AlumnoCursoModel(
                alumno = alumno.alumnoId,
                curso = curso.cursoId
            )
            matricula.save()
            self.assertEqual('{} {}'.format(matricula.registroAlumno.alumnoNombre, matricula.registroAlumno.alumnoApellido), 'Walter Emiliano Gonzales Inga')
            self.assertEqual(matricula.registroCurso.query.first().cursoNombre, 'CURSO DE PRUEBA')
            expected = {
                'dni': '25578190',
                'nombre': 'Walter Emiliano', 
                'apellido': 'Gonzales Inga', 
                'direccion': 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100', 
                'pais': 'Peru', 
                'fecha_nacimiento': '1970-11-01', 
                'cursos': ['CURSO DE PRUEBA']
                }
            result = {
                i: matricula.registroAlumno.join_json().get(i) 
                for i in ['dni', 'nombre', 'apellido', 'direccion', 'pais', 'fecha_nacimiento', 'cursos']
                }
            self.assertDictEqual(result, expected)
            matricula.delete()
            curso.delete()
            alumno.delete()

