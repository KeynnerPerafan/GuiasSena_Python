# models.py

from mongoengine import Document, StringField, DateTimeField, ReferenceField
from flask_login import UserMixin
from datetime import datetime

# Modelo de Instructor
class Instructor(UserMixin, Document):
    nombre = StringField(required=True)
    correo = StringField(required=True, unique=True)
    regional = StringField(required=True)
    password = StringField(required=True)

    meta = {'collection': 'instructores'}

    def get_id(self):
        return str(self.id)

# Modelo de Guía de Aprendizaje
class GuiaAprendizaje(Document):
    nombre_guia = StringField(required=True)
    descripcion = StringField(required=True)
    programa = StringField(required=True)
    archivo_pdf = StringField(required=True)  # ruta del archivo
    fecha_subida = DateTimeField(default=datetime.utcnow)
    instructor = ReferenceField(Instructor)

    meta = {'collection': 'guias'}

# models.py

from mongoengine import Document, StringField

class Regional(Document):
    nombre = StringField(required=True, unique=True)
    meta = {'collection': 'regionales'}

class Programa(Document):
    nombre = StringField(required=True, unique=True)
    meta = {'collection': 'programas'}