
# URL
from django.shortcuts import render, get_object_or_404, redirect

# UUID
import uuid

# Modelo
from apps.actividades.models import DocumentoNotificacionCliente

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo



# MENSAJES
from django.contrib import messages

def cerrar_pestana(request):
    template_name = 'cerrar_pestania.html'
    return render(request, 'cerrar_pestania.html')


def es_uuid_valido(valor):
    try:
        uuid_obj = uuid.UUID(str(valor))
        return True
    except (ValueError, TypeError):
        return False
    
@login_required
@usuario_activo
def validar_documento(request, id):
    documento_ha_validar = DocumentoNotificacionCliente.objects.filter(id=id).first()

    if documento_ha_validar is None:
        return redirect('actividades:cerrar_pestania')
    
    if documento_ha_validar.status:
        return redirect('actividades:cerrar_pestania')
    
    documento_ha_validar.status = True
    documento_ha_validar.save()

    messages.success(request, 'Registrar Boleta')

    return redirect('financings:create_payment_credit', documento_ha_validar.cuota.credit_id.id )
