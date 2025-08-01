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
@permiso_requerido('puede_crear_registro_cobranza')
def creacion_cobranza(request):
    template_name = 'cobranza/create.html'

    informe_usuario = Informe.objects.filter(
        usuario=request.user,
        esta_activo=True
    ).first()

    if informe_usuario is None:
        informe_usuario = Informe.objects.create(
            usuario=request.user,
            esta_activo=True,
            nombre_reporte=f'INVERSIONES INTEGRALES EL TELAR'
        )

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is None:
        return redirect('index')

    if request.method == 'POST':
        form = CobranzaForms(request.POST)

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
            fcobranza.fecha_limite_cuota = info_cuota.mostrar_fecha_limite().date()
            fcobranza.cuota = info_cuota
            fcobranza.asesor_credito = asesor_autenticado
            fcobranza.save()

            DetalleInformeCobranza.objects.create(
                reporte = informe_usuario,
                cobranza = fcobranza
            )
            messages.success(request, "Registro Completado Con Exito.")
            return redirect('customers:cobranza_asesor')
    else:
        form = CobranzaForms()

            

    context = {
        'title': f'Registro de Cobranza | {asesor_autenticado} |',
        'form': form,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)