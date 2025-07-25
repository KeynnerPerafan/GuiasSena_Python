# app.py

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from mongoengine import connect
from config import Config
from models import Instructor
import os

app = Flask(__name__)
app.config.from_object(Config)

# Conexión con MongoDB usando URI desde .env
connect(host=os.getenv("URI"))

# Configurar login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Configurar correo
mail = Mail(app)

# Cargar rutas
from routes import *

# Ejecutar solo si es ejecución directa
if __name__ == '__main__':
    app.run(debug=True)
