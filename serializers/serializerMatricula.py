from flask_restful import Resource, reqparse

serializerMatricula = reqparse.RequestParser(bundle_errors=True)

serializerMatricula.add_argument(
    'id_alumno',
    type=int,
    required=True,
    help='Id del alumno obligatorio',
    location='json'
)
serializerMatricula.add_argument(
    'id_curso',
    type=int,
    required=True,
    help='Id del curso obligatorio',
    location='json'
)