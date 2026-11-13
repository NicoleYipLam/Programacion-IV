import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar extensiones globalmente
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Clave secreta necesaria para los mensajes Flash y sesiones
    app.config['SECRET_KEY'] = 'clave-secreta-super-segura-12345'
    
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de Mailtrap desde el archivo .env
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 2525))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    mail.init_app(app)

    # Sincronizar la configuración con Celery
    from celery_app import celery
    celery.flask_app = app
    celery.conf.update(app.config)

    # Registrar el Blueprint de las rutas
    from app.routes import bp
    app.register_blueprint(bp)

    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        from app import models
        db.create_all()

    return app