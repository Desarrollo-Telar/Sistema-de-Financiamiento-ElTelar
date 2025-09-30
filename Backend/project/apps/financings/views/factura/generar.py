from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Payment, PaymentPlan, AccountStatement, Recibo
from apps.financings.models import Invoice, Credit

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.INFILE.fact import guardar_xml_recibo

# FORMULARIO
from apps.financings.forms import PaymentPlanForms, BoletaForm

# Manejo de mensajes
from django.contrib import messages

@login_required
@usuario_activo
def generar_factura(request,id):
    recibo = get_object_or_404(Recibo, id=id)

    if not recibo.factura:
        recibo.factura = True
        recibo.save()
    
        ruta_guardado = guardar_xml_recibo(
            recibo, 
            nombre_archivo=f"recibo_{recibo.id}_{recibo.fecha.strftime('%Y%m%d')}.xml"
        )
        print(ruta_guardado)

        messages.success(request, 'Factura Creada')
    

    return redirect('financings:detail_credit',recibo.pago.credit.id)