from models.alumno import AlumnoModel
from test.unit.base_test import BaseTest
from uuid import uuid4
from datetime import datetime

class AlumnoTest(BaseTest):
    def test_alumnoModel(self):
        with self.app_context:
            alumno = AlumnoModel(
                matricula = uuid4(),
                nombre = 'Jose Gabriel',
                apellido = 'Gonzales Ramos',
                direccion = 'Freire 2197 Piso 6 Camarones, Región de Arica y Parinacota, 1664830',
                pais = 'Peru',
                fecha_nacimiento = datetime.strptime('1999-02-25',"%Y-%m-%d")
                )
            self.assertIsNone(AlumnoModel.query.filter_by(alumnoNombre='Jose Gabriel').first())
            alumno.save()
            self.assertIsNotNone(AlumnoModel.query.filter_by(alumnoNombre='Jose Gabriel').first())
            alumno.delete()
            self.assertIsNone(AlumnoModel.query.filter_by(alumnoNombre='Jose Gabriel').first())
            