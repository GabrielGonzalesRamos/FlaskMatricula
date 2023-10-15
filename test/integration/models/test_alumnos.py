from models.alumno import AlumnoModel
from test.unit.base_test import BaseTest
from test.helper import data_alumno
import json

class AlumnoTest(BaseTest):
    def test_alumnoModel(self):
        data = json.loads(data_alumno()).values()
        with self.app_context():
            alumno = AlumnoModel(*data)
            alumno.save()
            self.assertTrue(AlumnoModel.query.all())
            alumno.delete()
            self.assertFalse(AlumnoModel.query.all())


