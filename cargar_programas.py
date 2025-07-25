from mongoengine import connect
from models import Programa

# Conexión a tu base de datos
connect(db="GuiasSena", host="mongodb+srv://kperafan:1234@cluster0.otk1lch.mongodb.net/GuiasSena?retryWrites=true&w=majority&appName=Cluster0<")

# Lista de programas
programas = [
    "Desarrollo de Software",
    "Multimedia",
    "Inteligencia Artificial",
    "Analítica de Datos",
    "Construcción",
    "Contabilidad"
]

# Insertar solo si no existe
for nombre in programas:
    if not Programa.objects(nombre=nombre).first():
        Programa(nombre=nombre).save()
        print(f"Programa '{nombre}' insertado.")
    else:
        print(f"Programa '{nombre}' ya existe.")
