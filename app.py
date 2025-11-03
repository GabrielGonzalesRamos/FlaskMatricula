from flask import Flask
from os import environ
from dotenv import load_dotenv
from config.conexion_bd import base_de_datos
from flask_restful import Api
from controllers.alumnos import AlumnosController, AlumnoController, BusquedaAlumnos
from controllers.cursos import CursosController, CursoController, BusquedaCursos
from controllers.matricula import MatriculaController
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from elasticapm.contrib.flask import ElasticAPM
import logging
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

swagger_blueprint=get_swaggerui_blueprint(
    "",
    "/static/swagger.json",
    config={
        'app_name': "SISTEMA DE MATRICULAS - SWAGGER DOCUMENTATION"
    }
    
)

app = Flask(__name__)
api = Api(app)

app.register_blueprint(swagger_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI_PROD') if environ.get('ENVIRONMENT') == 'PROD' else environ.get('DATABASE_URI_DEV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
base_de_datos.init_app(app)
base_de_datos.create_all(app=app)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-api-matriculas',  
    'SERVER_URL': 'http://192.168.100.123:8200/',
    'ENVIRONMENT': 'development',
    'DEBUG': True,  
}
apm = ElasticAPM(app)




api.add_resource(AlumnosController, '/alumnos')
api.add_resource(AlumnoController, '/alumno/<int:id>')
api.add_resource(BusquedaAlumnos, '/busqueda_alumnos')
api.add_resource(CursosController, '/cursos')
api.add_resource(CursoController, '/curso/<int:id>')
api.add_resource(BusquedaCursos, '/busqueda_cursos')
api.add_resource(MatriculaController, '/matricula')

CORS(app=app, methods=['GET', 'POST', 'PUT', 'DELETE'], origins=['*'], allow_headers=['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
    