from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from app import app, mail, login_manager
from models import Instructor, GuiaAprendizaje
from forms import RegistroForm, LoginForm, SubirGuiaForm
from werkzeug.utils import secure_filename
from datetime import datetime
import os


# Cargar usuario por ID
@login_manager.user_loader
def load_user(user_id):
    return Instructor.objects(id=user_id).first()


# Página de inicio
@app.route('/')
def index():
    return redirect(url_for('login'))


# Registro de instructores
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        if Instructor.objects(correo=form.correo.data).first():
            flash('Ya existe un instructor con ese correo.', 'danger')
            return redirect(url_for('register'))

        instructor = Instructor(
            nombre=form.nombre.data,
            correo=form.correo.data,
            regional=form.regional.data,
            password=form.password.data
        )

        instructor.save()

        # Enviar correo con credenciales
        msg = Message('Registro exitoso - Plataforma de Guías',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[instructor.correo])
        msg.body = f"""Hola {instructor.nombre},

Te has registrado correctamente en la plataforma.

Tus credenciales son:
Usuario: {instructor.correo}
Contraseña: {instructor.password}

Saludos,
Equipo de Desarrollo
"""
        mail.send(msg)

        flash('Registro exitoso. Revisa tu correo.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        instructor = Instructor.objects(correo=form.correo.data).first()
        if instructor and instructor.password == form.password.data:
            login_user(instructor)
            flash(f'Bienvenido, {instructor.nombre}', 'success')
            return redirect(url_for('listar_guias'))  # Redirige al listado de guías
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html', form=form)


# Cierre de sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for('login'))


# Subir guía
@app.route('/subir-guia', methods=['GET', 'POST'])
@login_required
def subir_guia():
    form = SubirGuiaForm()
    if form.validate_on_submit():
        archivo = form.archivo_pdf.data
        filename = secure_filename(archivo.filename)

        # Asegurar carpeta 'uploads' exista
        ruta_carpeta = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        # Ruta absoluta para guardar
        ruta_absoluta = os.path.join(ruta_carpeta, filename)
        archivo.save(ruta_absoluta)

        # Guardar solo nombre de archivo (sin ruta completa)
        guia = GuiaAprendizaje(
            nombre_guia=form.nombre_guia.data,
            descripcion=form.descripcion.data,
            programa=form.programa.data,
            archivo_pdf=filename,  # solo el nombre del archivo
            fecha_subida=datetime.utcnow(),
            instructor=current_user._get_current_object()
        )
        guia.save()

        flash('Guía subida correctamente', 'success')
        return redirect(url_for('listar_guias'))

    return render_template('upload.html', form=form)


# Listar guías
@app.route('/guias')
@login_required
def listar_guias():
    guias = GuiaAprendizaje.objects().order_by('-fecha_subida')
    return render_template('guides.html', guias=guias)


# Servir archivos PDF desde /uploads
@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/eliminar-guia/<guia_id>', methods=['POST'])
@login_required
def eliminar_guia(guia_id):
    guia = GuiaAprendizaje.objects(id=guia_id).first()
    if guia:
        # Eliminar archivo físico si existe
        ruta_pdf = os.path.join('uploads', guia.archivo_pdf)
        if os.path.exists(ruta_pdf):
            os.remove(ruta_pdf)

        # Eliminar registro en la base de datos
        guia.delete()
        flash('Guía eliminada correctamente.', 'success')
    else:
        flash('Guía no encontrada.', 'danger')

    return redirect(url_for('listar_guias'))

