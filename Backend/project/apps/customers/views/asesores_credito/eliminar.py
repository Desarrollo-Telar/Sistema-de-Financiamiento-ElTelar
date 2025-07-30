from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza
from apps.financings.models import PaymentPlan, Credit
from django.db.models import Q

# Formulario
from apps.customers.forms import CobranzaForms

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# MENSAJES
from django.contrib import messages

# Tiempo
from datetime import datetime,timedelta

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_informacion.detalle_asesor_credito import recoleccion_informacion_detalle_asesor

@login_required
def eliminacion_cobranza(request, id):
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is None:
        return redirect('index')
    
    cobranza = Cobranza.objects.filter(asesor_credito=asesor_autenticado, id=id).first()

    if cobranza is None:
        return redirect('index')
    
    informe_usuario = DetalleInformeCobranza.objects.filter(
        cobranza=cobranza
    ).first()

    if not informe_usuario.reporte.esta_activo:
        messages.error(request, 'El perido de esta cobranza ya ha pasado, no se puede realizar ninguna eliminacion')
        return redirect('index')
    
    cobranza.delete()
    messages.success(request, 'Registro Eliminado')
    return redirect('customers:detail_informe_cobranza', request.user.user_code,informe_usuario.reporte.id )