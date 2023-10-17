import json
from datetime import datetime
from faker import Faker
from random import randint, choice
from string import digits

fake = Faker(['es_MX', 'es_AR', 'es_CL', 'es_CO'])

def data_alumno():
    return json.dumps({
        'dni': ''.join(choice(digits) for i in range(1, 9)),
        'nombre': fake.first_name(),
        'apellido': '{} {}'.format(fake.last_name(), fake.last_name()),
        'direccion': fake.address(),
        'pais': fake.current_country(),
        'fecha_nacimiento': fake.date_between_dates(date_start=datetime(1990, 1, 1), date_end=datetime(2000, 12, 31)).strftime("%Y-%m-%d")
    })

def data_alumno_error():
    return json.dumps({
        'dni': ''.join(choice(digits) for i in range(1, 10)),
        'nombre': fake.first_name(),
        'apellido': '{} {}'.format(fake.last_name(), fake.last_name()),
        'direccion': fake.address(),
        'pais': fake.current_country(),
        'fecha_nacimiento': fake.date_between_dates(date_start=datetime(1990, 1, 1), date_end=datetime(2000, 12, 31)).strftime("%Y-%m-%d")
    })

def data_curso():
    return json.dumps({
        'nombre': '{} {}'.format('CURSO DE PRUEBA', randint(1, 10001)),
        'fecha_inicio': fake.date_between_dates(date_start=datetime(2023, 1, 1), date_end=datetime(2023, 1, 31)).strftime("%Y-%m-%d"),
        'fecha_fin': fake.date_between_dates(date_start=datetime(2023, 2, 1), date_end=datetime(2023, 2, 28)).strftime("%Y-%m-%d")        
    })

def data_curso_error():
    return json.dumps({
        'nombre': '{} {}'.format('CURSO DE PRUEBA', randint(1, 10001)),
        'fecha_inicio': fake.date_between_dates(date_start=datetime(2023, 2, 1), date_end=datetime(2023, 2, 28)).strftime("%Y-%m-%d"),
        'fecha_fin': fake.date_between_dates(date_start=datetime(2023, 1, 1), date_end=datetime(2023, 1, 31)).strftime("%Y-%m-%d")        
    })

def data_matricula(id_alumno, id_curso):
    return json.dumps({
        'id_alumno': id_alumno,
        'id_curso': id_curso
    })

def create_alumno(app):
    data = data_alumno()
    request = app().post('/alumnos', data = data, headers={'Content-Type': 'application/json'})
    return json.loads(request.data).get('content')


def create_curso(app):
    data = data_curso()
    app().post('/cursos', data = data, headers={'Content-Type': 'application/json'})



def create_matricula(app, id_alumno, id_curso):
    data = data_matricula(id_alumno, id_curso)
    request = app().post('/matricula', data = data, headers={'Content-Type': 'application/json'})
    return json.loads(request.data).get('message')