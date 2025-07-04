# URL
from django.shortcuts import render, get_object_or_404

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Modelos
from .models import Permiso, CategoriaPermiso
from apps.users.models import User, PermisoUsuario

# CONFIGURACION
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@permiso_requerido('puede_asignar_permisos_usuario')
def asignacion_permisos(request, user_id):
    template_name = 'permisos/agregar.html'

    usuario = get_object_or_404(User, pk=user_id)
    todos_permisos = Permiso.objects.all()
    permisos_asignados = PermisoUsuario.objects.filter(user=usuario).values_list('permiso_id', flat=True)

    context = {
        'usuario': usuario,
        'permisos': recorrer_los_permisos_usuario(request),
        'permisos_asignados': list(permisos_asignados),
        'todos_permisos':todos_permisos,
        'categorias_permisos': CategoriaPermiso.objects.all()
    }

    return render(request, template_name, context)

@csrf_exempt
@login_required
@permiso_requerido('puede_asignar_permisos_usuario')
def guardar_permisos_usuario(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(User, pk=user_id)
        data = json.loads(request.body)
        nuevos_permisos = data.get('permisos', [])

        # Eliminar permisos anteriores
        PermisoUsuario.objects.filter(user=usuario).delete()

        # Crear nuevos
        for permiso_id in nuevos_permisos:
            permiso = get_object_or_404(Permiso, pk=permiso_id)
            PermisoUsuario.objects.create(user=usuario, permiso=permiso)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)