from celery_app import celery
from app import mail
from flask_mail import Message

@celery.task
def enviar_correo_agregar(email_destino, titulo_libro):
    msg = Message(
        subject="📖 Libro Agregado Exitosamente",
        sender="noreply@library.com",
        recipients=[email_destino]
    )
    msg.body = f"¡Hola! El libro '{titulo_libro}' ha sido registrado correctamente en tu biblioteca personal."
    mail.send(msg)

@celery.task
def enviar_correo_eliminar(email_destino, titulo_libro):
    msg = Message(
        subject="🗑️ Libro Eliminado de la Biblioteca",
        sender="noreply@library.com",
        recipients=[email_destino]
    )
    msg.body = f"Aviso: El libro '{titulo_libro}' ha sido eliminado de tu biblioteca personal."
    mail.send(msg)