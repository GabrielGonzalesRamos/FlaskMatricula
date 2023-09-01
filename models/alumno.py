from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm, UniqueConstraint, CheckConstraint


class AlumnoModel(base_de_datos.Model):
    __tablename__ = 'TB_ALUMNO'
    alumnoId = Column(name='ID',autoincrement=True, primary_key=True, unique=True, type_=types.Integer, nullable=False)
    alumnoDNI = Column(name='DNI', unique=True, type_=types.String(length=8), nullable=False)
    alumnoNombre = Column(name='NOMBRE', type_=types.String(length=45))
    alumnoApellido = Column(name='APELLIDO', type_=types.String(length=45))
    alumnoDireccion = Column(name='DIRECCION', type_=types.String(length=200))
    alumnoPais = Column(name='PAIS', type_=types.String(length=200))
    alumnoFechaNacimiento = Column(name='FECHA_NACIMIENTO', type_=types.Date)

    alumnoRegistrados = orm.relationship('AlumnoCursoModel', backref='registroAlumno', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('NOMBRE', 'APELLIDO', 'DNI', name='avoid_duplicate_tb_alumno'),
        CheckConstraint('DNI LIKE "%[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]%"', name='only_numbers_8_tb_alumno')
        )

    def __init__(self, nombre, apellido, dni, direccion, pais, fecha_nacimiento):
        self.alumnoNombre = nombre
        self.alumnoApellido = apellido
        self.alumnoDNI = dni
        self.alumnoDireccion = direccion
        self.alumnoPais = pais
        self.alumnoFechaNacimiento = fecha_nacimiento

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
    
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()
    
    def json(self):
        return {
            'id': self.alumnoId,
            'dni': self.alumnoDNI,
            'nombre': self.alumnoNombre,
            'apellido': self.alumnoApellido,
            'direccion': self.alumnoDireccion,
            'pais': self.alumnoPais,
            'fecha_nacimiento': self.alumnoFechaNacimiento.strftime('%Y-%m-%d')
        }

    def join_json_id(self, id):
        return {
            'id': self.alumnoId,
            'dni': self.alumnoDNI,
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
            'dni': self.alumnoDNI,
            'nombre': self.alumnoNombre,
            'apellido': self.alumnoApellido,
            'direccion': self.alumnoDireccion,
            'pais': self.alumnoPais,
            'fecha_nacimiento': self.alumnoFechaNacimiento.strftime('%Y-%m-%d'),
            'cursos': [i.cursoNombre for i in [i.registroCurso for i in self.alumnoRegistrados]]            
        }
