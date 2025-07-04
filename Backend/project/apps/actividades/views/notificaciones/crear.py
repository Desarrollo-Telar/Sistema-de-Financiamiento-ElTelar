
# Formulario
from apps.actividades.forms.documentoBoletaCliente import DocumentoNotificacionClienteForms

# Token
from apps.codes.models import TokenCliente

# Relacion
from apps.actividades.models import DocumentoNotificacionCliente

# URL
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# MENSAJES
from django.contrib import messages

# Funcionalidades
from .funcionalidades import es_uuid_valido

def subida_documento(request, uuid):
    # Validar si esta pasando el token correctamente
    if not es_uuid_valido(uuid):
        return redirect('actividades:cerrar_pestania')

    # Obtener el token del cliente
    token_cliente = TokenCliente.objects.filter(uuid=uuid).first()

    # Validar que exista registro del token
    if token_cliente is None:
        return redirect('actividades:cerrar_pestania')
    
    # Cargar Formulario
    form = DocumentoNotificacionClienteForms

    
    # Buscar si ya hay un registro de documento
    documento_cliente = DocumentoNotificacionCliente.objects.filter(cliente = token_cliente.cliente, cuota=token_cliente.cuota ).first()

    if documento_cliente.status:
        token_cliente.delete() # Eliminar el token
        return redirect('actividades:cerrar_pestania')


    if documento_cliente is not None:
        form = DocumentoNotificacionClienteForms(instance=documento_cliente) # Cargar con los documentos ya subidos
     
    if request.method == 'POST':
        form = DocumentoNotificacionClienteForms(request.POST, request.FILES)

        if documento_cliente is not None:
            form = DocumentoNotificacionClienteForms(request.POST, request.FILES,instance=documento_cliente) # Cargar con los documentos ya subidos

        
        if form.is_valid():
            documento = form.save(commit=False)
            documento.cliente = token_cliente.cliente
            documento.cuota = token_cliente.cuota
            documento.save()
            messages.success(request, 'Se ha subido correctamente su documento. ')
            return redirect('actividades:cerrar_pestania')




    # Estructura de la vista
    template_name = 'customer/documentoNotificacionCliente.html'
    context = {
        'form':form,
    }
    return render(request, template_name, context)