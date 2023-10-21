from os import environ
from dotenv import load_dotenv
from unittest import TestCase
from app import app 
from config.conexion_bd import base_de_datos

load_dotenv()

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI_PROD') if environ.get('ENVIRONMENT') == 'PROD' else environ.get('DATABASE_URI_DEV')
        print(environ.get('ENVIRONMENT'))
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        base_de_datos.create_all(app=app)

    @classmethod
    def tearDownClass(cls):
        base_de_datos.drop_all(app=app)

    def setUp(self):
        self.app = app.test_client
        self.app_context = app.app_context