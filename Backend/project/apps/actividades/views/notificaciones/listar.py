
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

# Paginacion
from project.pagination import paginacion

@login_required
@usuario_activo
def listar_notificaciones(request):

    template_name = 'notification/list.html'
    notificacion = Notification.objects.filter(user=request.user).order_by('-created_at')

    page_obj = paginacion(request, notificacion)

    context = {
        'title':'Notificaciones',
        'object_list': page_obj,
        'permisos':recorrer_los_permisos_usuario(request),
        'page_obj':page_obj,
    }

    return render(request, template_name, context)
