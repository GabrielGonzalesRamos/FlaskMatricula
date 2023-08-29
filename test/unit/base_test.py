from os import environ
from dotenv import load_dotenv
from unittest import TestCase
from app import app 
from config.conexion_bd import base_de_datos

load_dotenv()

class BaseTest(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI_DEV')
        with app.app_context():
            base_de_datos.init_app(app)
            base_de_datos.create_all(app=app)

            self.app = app.test_client
            self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            base_de_datos.session.remove()
            base_de_datos.drop_all(app=app)
