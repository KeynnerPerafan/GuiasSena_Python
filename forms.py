from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from models import Regional, Programa 

# Formulario de registro de instructores
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    regional = SelectField('Regional', coerce=str, validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Carga dinámica de regionales desde la base de datos
        self.regional.choices = [(r.nombre, r.nombre) for r in Regional.objects()]


# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


# Formulario para subir guías
class SubirGuiaForm(FlaskForm):
    nombre_guia = StringField('Nombre de la Guía', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    programa = SelectField('Programa de Formación', coerce=str, validators=[DataRequired()])
    archivo_pdf = FileField('Archivo PDF', validators=[
        FileRequired(), FileAllowed(['pdf'], 'Solo archivos PDF')
    ])
    submit = SubmitField('Subir Guía')

    def __init__(self, *args, **kwargs):
        super(SubirGuiaForm, self).__init__(*args, **kwargs)
        # Carga dinámica de programas desde la base de datos
        self.programa.choices = [(p.nombre, p.nombre) for p in Programa.objects()]
