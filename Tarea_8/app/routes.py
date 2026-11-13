from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Libro
from app.tasks import enviar_correo_agregar, enviar_correo_eliminar

# Definir el Blueprint
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        email = request.form.get('email')
        
        # Guardar en la base de datos
        nuevo_libro = Libro(titulo=titulo, autor=autor, email=email)
        db.session.add(nuevo_libro)
        db.session.commit()
        
        # Disparar tarea asíncrona de Celery para AGREGAR
        enviar_correo_agregar.delay(email, titulo)
        flash('¡Libro agregado con éxito! Se ha enviado una notificación.', 'success')
        
        return redirect(url_for('main.index'))
        
    libros = Libro.query.all()
    return render_template('index.html', libros=libros)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    
    email_destino = libro.email
    titulo_libro = libro.titulo
    
    # Eliminar de la base de datos
    db.session.delete(libro)
    db.session.commit()
    
    # Disparar tarea asíncrona de Celery para ELIMINAR
    enviar_correo_eliminar.delay(email_destino, titulo_libro)
    flash('El libro ha sido eliminado y se ha enviado la notificación.', 'info')
    
    return redirect(url_for('main.index'))