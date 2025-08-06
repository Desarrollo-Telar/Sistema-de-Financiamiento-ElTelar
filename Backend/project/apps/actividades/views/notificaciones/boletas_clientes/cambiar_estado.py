
# Modelos
from apps.actividades.models import DocumentoNotificacionCliente

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
def aprobar_boleta_cliente(request, id):

    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()
    
    if detalle_boleta is None:
        return redirect('actividades:cerrar_pestania')
    
    detalle_boleta.status = True
    detalle_boleta.save()

  
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def rechazar_boleta_cliente(request, id):

    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()
    
    if detalle_boleta is None:
        return redirect('actividades:cerrar_pestania')
    
    detalle_boleta.status = False
    detalle_boleta.save()

  
    return redirect(request.META.get('HTTP_REFERER', '/'))