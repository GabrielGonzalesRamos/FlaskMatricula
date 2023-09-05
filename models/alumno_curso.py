from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types
from sqlalchemy.sql.schema import ForeignKey

class AlumnoCursoModel(base_de_datos.Model):
    __tablename__ = 'tb_alumno_curso'
    acIdAlumno = Column(ForeignKey(column='tb_alumno.id', onupdate='CASCADE', ondelete='CASCADE'), name='id_alumno', type_=types.Integer, primary_key=True, nullable=False)
    acIdCurso = Column(ForeignKey(column='tb_curso.id', onupdate='CASCADE', ondelete='CASCADE'),name='id_curso', type_=types.Integer, primary_key=True, nullable=False)

    def __init__(self, alumno, curso):
        self.acIdAlumno = alumno
        self.acIdCurso = curso
    
    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()
    
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()

    def json(self):
        return {
            'id_alumno': self.acIdAlumno,
            'id_curos': self.acIdCurso
        }
