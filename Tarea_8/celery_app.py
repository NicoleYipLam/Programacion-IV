import os
from celery import Celery, Task
from dotenv import load_dotenv

load_dotenv()

# 1. Definir la clase a nivel global (fuera de cualquier función) para que sea "picklable"
class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        if celery.flask_app:
            with celery.flask_app.app_context():
                return self.run(*args, **kwargs)
        return self.run(*args, **kwargs)

# 2. Inicializar Celery usando la clase global
celery = Celery(
    'app',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    task_cls=FlaskTask
)

# Atributo temporal para guardar la instancia de Flask
celery.flask_app = None