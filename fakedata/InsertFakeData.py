from faker import Faker
from datetime import datetime
from OdbcSQLSERVER import connection, cursor
from uuid import uuid4

fake = Faker(['es_MX', 'es_AR', 'es_CL', 'es_CO'])

def bdMatricula(alumnos):
    for i in range(1, int(alumnos) + 1):
        matricula = uuid4()
        nombre = f'{fake.first_name()}'
        apellido = f'{fake.last_name()} {fake.last_name()}'
        direccion =  fake.address()
        pais = fake.current_country() 
        fecha_nacimiento = fake.date_between_dates(date_start=datetime(1990,1,1), date_end=datetime(2000,12,31))
        try:
            cursor.execute(
                "INSERT INTO TB_ALUMNO(MATRICULA, NOMBRE, APELLIDO, DIRECCION, PAIS, FECHA_NACIMIENTO) VALUES (?, ?, ?, ?, ?, ?)", 
                matricula, nombre, apellido, direccion, pais, fecha_nacimiento
                )
            connection.commit()
        except Exception as E:
            print(E)

    with open('fakedata/cursos.txt', mode='r') as cursos:
        for i in cursos.readlines():
            fecha_inico = fake.date_between_dates(date_start=datetime(2023,1,1), date_end=datetime(2023,7,31))
            fecha_fin = fake.date_between_dates(date_start=fecha_inico, date_end=datetime(2023,7,31))
            try:
                cursor.execute( 
                    "INSERT INTO TB_CURSO(NOMBRE, FECHA_INICIO, FECHA_FIN) VALUES(?, ?, ?)",
                    i.strip(), fecha_inico, fecha_fin
                    )
                connection.commit()
            except Exception as E:
                print(E)

    id_min_alumno = cursor.execute('SELECT MIN(ID) FROM TB_ALUMNO').fetchone()[0]
    id_max_alumno = cursor.execute('SELECT MAX(ID) FROM TB_ALUMNO').fetchone()[0]
    id_min_curso = cursor.execute('SELECT MIN(ID) FROM TB_CURSO').fetchone()[0]
    id_max_curso = cursor.execute('SELECT MAX(ID) FROM TB_CURSO').fetchone()[0]

    contador = 1
    while contador <= (int(alumnos)*2):
        alumno = fake.random_int(min=int(id_min_alumno), max=int(id_max_alumno))
        curso = fake.random_int(min=int(id_min_curso), max=int(id_max_curso))
        try:
            cursor.execute(
                'INSERT INTO TB_ALUMNO_CURSO(ID_ALUMNO, ID_CURSO) VALUES(?, ?)', 
                alumno, curso
            )
            connection.commit()
            contador += 1
        except Exception as E:
            print(E)

bdMatricula(5000)



