from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm


class AlumnoModel(base_de_datos.Model):
    __tablename__ = 'TB_ALUMNO'
    alumnoId = Column(name='ID', primary_key=True, autoincrement=True, unique=True, type_=types.Integer, nullable=False)
    alumnoMatricula = Column(name='MATRICULA', unique=True, type_=types.String(length=45), nullable=False)
    alumnoNombre = Column(name='NOMBRE', type_=types.String(length=45))
    alumnoApellido = Column(name='APELLIDO', type_=types.String(length=45))
    alumnoDireccion = Column(name='DIRECCION', type_=types.String(length=200))
    alumnoPais = Column(name='PAIS', type_=types.String(length=200))
    alumnoFechaNacimiento = Column(name='FECHA_NACIMIENTO', type_=types.Date)
    
    alumnoRegistrados = orm.relationship('AlumnoCursoModel', backref='registroAlumno', lazy=True, cascade='all, delete-orphan')

    def __init__(self, nombre, apellido, direccion, pais, fecha_nacimiento, matricula):
        self.alumnoNombre = nombre
        self.alumnoApellido = apellido
        self.alumnoDireccion = direccion
        self.alumnoPais = pais
        self.alumnoFechaNacimiento = fecha_nacimiento
        self.alumnoMatricula = matricula

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
    
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()
    
    def json(self):
        return {
            'id': self.alumnoId,
            'matricula': self.alumnoMatricula,
            'nombre': self.alumnoNombre,
            'apellido': self.alumnoApellido,
            'direccion': self.alumnoDireccion,
            'pais': self.alumnoPais,
            'fecha_nacimiento': self.alumnoFechaNacimiento.strftime('%Y-%m-%d')
        }

    def join_json_id(self, id):
        return {
            'id': self.alumnoId,
            'matricula': self.alumnoMatricula,
            'nombre': self.alumnoNombre,
            'apellido': self.alumnoApellido,
            'direccion': self.alumnoDireccion,
            'pais': self.alumnoPais,
            'fecha_nacimiento': self.alumnoFechaNacimiento.strftime('%Y-%m-%d'),
            'cursos': [i.cursoNombre for i in [i.registroCurso for i in base_de_datos.session.query(AlumnoModel).filter_by(alumnoId=id).first().alumnoRegistrados]]
        }
        
    def join_json(self):
        return {
            'id': self.alumnoId,
            'matricula': self.alumnoMatricula,
            'nombre': self.alumnoNombre,
            'apellido': self.alumnoApellido,
            'direccion': self.alumnoDireccion,
            'pais': self.alumnoPais,
            'fecha_nacimiento': self.alumnoFechaNacimiento.strftime('%Y-%m-%d'),
            'cursos': [i.cursoNombre for i in [i.registroCurso for i in self.alumnoRegistrados]]            
        }
