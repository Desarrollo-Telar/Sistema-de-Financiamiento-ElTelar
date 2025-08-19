
# Modelos
from apps.actividades.models import DocumentoNotificacionCliente
from apps.financings.models import Payment

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
def detalle_boleta_cliente(request, id):
    template_name = 'customer/boletas_clientes/detalle.html'
    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()

    

    if detalle_boleta is None:
        return redirect('actividades:cerrar_pestania')


    context = {
        'permisos': recorrer_los_permisos_usuario(request),
        'object':detalle_boleta
    }
    return render(request, template_name, context)