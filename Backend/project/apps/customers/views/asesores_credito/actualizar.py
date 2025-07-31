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
def actualizacion_cobranza(request, id):
    template_name = 'cobranza/actualizar.html'
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
        messages.error(request, 'El perido de esta cobranza ya ha pasado, no se puede realizar ninguna actualizacion')
        return redirect('index')
    

    if request.method == 'POST':
        form = CobranzaForms(request.POST, instance=cobranza)

        if form.is_valid():
            fcobranza = form.save(commit=False)
            dia = datetime.now().date()
            dia_mas_uno = dia + timedelta(days=1)

            credito = Credit.objects.filter(id=fcobranza.credito.id).first()
            
            siguiente_pago = PaymentPlan.objects.filter(
                credit_id=credito,
                start_date__lte=dia,
                fecha_limite__gte=dia_mas_uno
            ).first()

            if siguiente_pago is None:
                siguiente_pago = PaymentPlan.objects.filter(
                credit_id=credito).order_by('-id').first()
            
            info_cuota = siguiente_pago

            fcobranza.cuota = info_cuota
            fcobranza.fecha_limite_cuota = info_cuota.mostrar_fecha_limite().date()
            fcobranza.asesor_credito = asesor_autenticado
            fcobranza.save()


            messages.success(request, "Registro Completado Con Exito.")
            return redirect('customers:detail_informe_cobranza', request.user.user_code,informe_usuario.reporte.id )
    else:
        form = CobranzaForms(instance=cobranza)

            

    context = {
        'title': f'Actualizacion de Cobranza | {asesor_autenticado} |',
        'form': form,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)