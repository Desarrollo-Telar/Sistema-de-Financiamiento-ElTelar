from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configura la ruta del archivo settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Instancia la aplicación Celery
app = Celery('project')

# Carga la configuración desde las settings de Django, usando un namespace específico 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre automáticamente las tareas definidas en los `tasks.py` de cada app
app.autodiscover_tasks()
app.autodiscover_tasks(['apps.financings'])
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
