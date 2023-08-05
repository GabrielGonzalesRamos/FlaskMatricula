from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types
from sqlalchemy.sql.schema import ForeignKey

class AlumnoCursoModel(base_de_datos.Model):
    __tablename__ = 'TB_ALUMNO_CURSO'
    acIdAlumno = Column(
        ForeignKey(column='TB_ALUMNO.ID', onupdate='CASCADE', ondelete='CASCADE'),
        name='ID_ALUMNO', type_=types.Integer, primary_key=True, nullable=False
        )
    acIdCurso = Column(
        ForeignKey(column='TB_CURSO.ID', onupdate='CASCADE', ondelete='CASCADE'),
        name='ID_CURSO', type_=types.Integer, primary_key=True, nullable=False
        )

    def __init__(self, alumno, curso):
        self.acIdAlumno = alumno
        self.acIdCurso = curso
        
