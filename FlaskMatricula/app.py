from flask import Flask, request
from os import environ
from dotenv import load_dotenv
from config.conexion_bd import base_de_datos
from models.alumno import AlumnoModel
from models.curso import CursoModel
from models.alumno_curso import AlumnoCursoModel

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_de_datos.init_app(app)
base_de_datos.create_all(app=app)

if __name__ == '__main__':
    app.run(debug=True)