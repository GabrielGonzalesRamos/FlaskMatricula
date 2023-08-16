from flask_restful import Resource, reqparse
from datetime import datetime

serializerCursos = reqparse.RequestParser(bundle_errors=True)

serializerCursos.add_argument(
    'nombre',
    type=lambda x: x.upper(),
    required=True,
    help='Nombre del curso obligatorio',
    location='json'
)

serializerCursos.add_argument(
    'fecha_inicio',
    type=lambda x: datetime.strptime(x, "%Y-%m-%d"),
    required=True,
    help='Fecha de inicio del curso obligatorio',
    location='json'
)

serializerCursos.add_argument(
    'fecha_fin',
    type=lambda x: datetime.strptime(x, "%Y-%m-%d"),
    required=True,
    help='Fecha fin del curso obligatorio',
    location='json'
)