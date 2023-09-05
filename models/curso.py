from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm, UniqueConstraint, CheckConstraint

class CursoModel(base_de_datos.Model):
    __tablename__ = 'tb_curso'
    cursoId = Column(name='id', primary_key=True, autoincrement=True, unique=True, type_=types.Integer, nullable=False)
    cursoNombre = Column(name='nombre', unique=True, type_=types.String(length=100), nullable=False)
    cursoFechaInicio = Column(name='fecha_inicio', type_=types.Date)
    cursoFechaFin = Column(name='fecha_fin', type_=types.Date)

    cursoRegistrados = orm.relationship('AlumnoCursoModel', backref='registroCurso', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('nombre', name='avoid_duplicate_tb_curso'),
        CheckConstraint('fecha_inicio < fecha_fin')
    )

    def __init__(self, nombre, fecha_inicio, fecha_fin):
        self.cursoNombre = nombre
        self.cursoFechaInicio = fecha_inicio
        self.cursoFechaFin = fecha_fin

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
    
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()
    
    def json(self):
        return {
            'id': self.cursoId,
            'nombre': self.cursoNombre,
            'fecha_inicio': self.cursoFechaInicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.cursoFechaFin.strftime('%Y-%m-%d')
        }
    
    def join_json(self):
        return {
            'id': self.cursoId,
            'nombre': self.cursoNombre,
            'fecha_inicio': self.cursoFechaInicio.strftime('%Y-%m-%d'),
            'fecha_fin': self.cursoFechaFin.strftime('%Y-%m-%d'),
            'alumnos_inscritos': [{'id': i.alumnoId, 'dni': i.alumnoDNI,'nombre': i.alumnoNombre, 'apellido': i.alumnoApellido, 'pais': i.alumnoPais} for i in [i.registroAlumno for i in self.cursoRegistrados]]
        }