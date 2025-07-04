
# Modelos
from apps.actividades.models import Notification

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario



# Funcionalidades
from .funcionalidades import es_uuid_valido

@login_required
@usuario_activo
def detalle_notificacion(request, uuid):

    if not es_uuid_valido(uuid):
        return redirect('actividades:cerrar_pestania')

    template_name = 'notification/detalle.html'
    notificacion = Notification.objects.filter(uuid=uuid).first()
    notificacion.read = True
    notificacion.save()
 

    context = {
        'title':f'Notificaciones| {uuid} |',
        'object': notificacion,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request, template_name, context)
