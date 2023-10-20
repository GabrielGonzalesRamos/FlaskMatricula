import os
from unittest import TestCase
from app import app 
from config.conexion_bd import base_de_datos

print(os.getenv('GITHUB_ENV'))

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI_DEV')
        base_de_datos.create_all(app=app)

    @classmethod
    def tearDownClass(cls):
        base_de_datos.drop_all(app=app)

    def setUp(self):
        self.app = app.test_client
        self.app_context = app.app_context