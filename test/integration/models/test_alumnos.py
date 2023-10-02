from models.alumno import AlumnoModel
from test.unit.base_test import BaseTest
from datetime import datetime

class AlumnoTest(BaseTest):
    def test_alumnoModel(self):
        with self.app_context():
            alumno = AlumnoModel(
                dni = '25578190',
                nombre = 'Walter Emiliano',
                apellido = 'Gonzales Inga',
                direccion = 'Calle Claudia Sánchez 3974 Tucapel, Región del Biobí, 0637100',
                pais = 'Peru',
                fecha_nacimiento = datetime.strptime('1970-11-01',"%Y-%m-%d")
                )
            self.assertIsNone(AlumnoModel.query.filter_by(alumnoNombre='Walter Emiliano').first())
            alumno.save()
            self.assertIsNotNone(AlumnoModel.query.filter_by(alumnoNombre='Walter Emiliano').first())
            alumno.delete()
            self.assertIsNone(AlumnoModel.query.filter_by(alumnoNombre='Walter Emiliano').first())