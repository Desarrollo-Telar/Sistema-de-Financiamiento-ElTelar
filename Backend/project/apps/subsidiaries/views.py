from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from .models import Subsidiary
from apps.addresses.models import Address



# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion


# MENSAJES
from django.contrib import messages

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Create your views here.

@login_required
def view_clasificacion(request):
    template_name = 'sucursal/clasificacion.html'
    sucursales = Subsidiary.objects.filter(activa=True).order_by('id')
    direccion_sucursal = Address.objects.filter(type_address='Dirección de Sucursal')

    sucursal = getattr(request,'sucursal_actual',None)
    
    if sucursal is not None:
        return redirect('index')


    context = {
        'sucursales':sucursales,
        'direccion_sucursal':direccion_sucursal,

    }
    return render(request, template_name, context)

@login_required
def view_seleccionado(request, id):
    sucursal = Subsidiary.objects.filter(id=id).first()
    if sucursal is None:
        return redirect('sucursal:clasificacion')

    request.session['sucursal_id'] = sucursal.id

    log_user_action(request.user,
                    'ELECCION DE OFICINA', 
                    f'El usuario {request.user} escogio la oficina: {request.session['sucursal_id']}',
                    request, 'SUCURSAL')

    return redirect('index')
