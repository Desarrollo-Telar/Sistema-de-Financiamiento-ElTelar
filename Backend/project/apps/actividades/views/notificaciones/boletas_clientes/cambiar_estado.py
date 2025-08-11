
# Modelos
from apps.actividades.models import DocumentoNotificacionCliente

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Formulario
from apps.actividades.forms.documentoBoletaCliente import DocumentoNotificacionClienteReferenciaForms

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# MENSAJES
from django.contrib import messages

@login_required
def aprobar_boleta_cliente(request, id):

    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()
    
    if detalle_boleta is None:
        return redirect('actividades:cerrar_pestania')
    
    if detalle_boleta.status:
        return redirect('actividades:detalle_boleta_cliente', detalle_boleta.id)

    if detalle_boleta.numero_referencia == '3696008759':
        messages.error(request, 'Esta Boleta no se puede validar, debido a que esta boleta pertenece a otra boleta, por favor cambie el numero de referencia')
        return redirect('actividades:cambio_referencia_boleta', detalle_boleta.id)
    
    detalle_boleta.status = True
    detalle_boleta.save()

    return redirect('actividades:detalle_boleta_cliente', detalle_boleta.id)


@login_required
def rechazar_boleta_cliente(request, id):

    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()
    
    if detalle_boleta is None:
        return redirect('actividades:cerrar_pestania')
    
    if detalle_boleta.status:
        return redirect('actividades:detalle_boleta_cliente', detalle_boleta.id)
    
    detalle_boleta.status = False
    detalle_boleta.save()

  
    return redirect('actividades:detalle_boleta_cliente', detalle_boleta.id)

@login_required
def cambio_referencia_boleta(request, id):
    detalle_boleta = DocumentoNotificacionCliente.objects.filter(id=id).first()
    template_name = 'customer/boletas_clientes/actualizar.html'

    form = DocumentoNotificacionClienteReferenciaForms(instance=detalle_boleta)
    if request.method == 'POST':
        form = DocumentoNotificacionClienteReferenciaForms(request.POST, request.FILES,instance=detalle_boleta)

        if form.is_valid():
            documento = form.save(commit=False)
            num_referencia = form.cleaned_data.get('numero_referencia')

            if num_referencia is None:
                messages.error(request, 'No se puede dejar el numero de referencia en blanco')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            if num_referencia == '3696008759':
                messages.error(request, 'Esta Referencia Es El Numero de Cuenta del Banco')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            documento.save()

            return redirect('actividades:aprobar_boleta_cliente', detalle_boleta.id)
            

    context = {
        'form':form
    }


    return render(request, template_name, context)