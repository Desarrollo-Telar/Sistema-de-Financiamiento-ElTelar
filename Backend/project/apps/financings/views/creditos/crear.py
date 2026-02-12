from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Models
from apps.financings.models import Credit
from apps.subsidiaries.models import Subsidiary

# Formularios
from apps.financings.forms import CreditoForms, PaymentPlanForms
from decimal import Decimal
# TIEMPO
from datetime import datetime, date

from .funciones import generar_codigo_seguridad

@login_required
@permiso_requerido('puede_crear_informacion_credito')
def create_credit(request):
    template_name = 'financings/credit/create.html'
    sucursal = request.session['sucursal_id']

    context = {
        'title':'Creacion de un Credito Nuevo.',
        'sucursal_id':sucursal,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)




@login_required
@permiso_requerido('puede_migrar_credito')
def migracion_creditos(request):
    template_name = 'financings/credit/migracion.html'
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])
    dia = datetime.now()
    mes = dia.month
    anio = dia.year

    form = CreditoForms
    form_cuota = PaymentPlanForms

    num = generar_codigo_seguridad(usuario_regis=request.user, accion='Migración de Credito.')
    request.session['codigo_migracion'] = num
    

   

    if request.method == 'POST':
        form = CreditoForms(request.POST)
        form_cuota = PaymentPlanForms(request.POST)
        
        

        if form.is_valid() and form_cuota.is_valid():
            
            credito = form.save(commit=False)
            cuota = form_cuota.save(commit=False)


            credito.es_credito_migrado = True
            credito.sucursal = sucursal
            credito.estados_fechas = None
            tasa_interes = Decimal(credito.tasa_interes) * Decimal(100)

            if tasa_interes <= 0 :
                credito.tasa_interes = 0.0
                credito.forma_de_pago = 'AMORTIZACIONES A CAPITAL'


            

            
            cuota.outstanding_balance = credito.monto
            cuota.sucursal= sucursal

            nuevo_dia = credito.fecha_inicio.day

            cuota.original_day = nuevo_dia
            try:
                cuota.start_date = date(anio, mes, nuevo_dia)
            except ValueError:
                # Si el día no existe en el mes actual (ej: 31 de febrero),
                # se ajusta al último día del mes actual.
                import calendar
                ultimo_dia = calendar.monthrange(anio, mes)[1]
                cuota.start_date = date(anio, mes, ultimo_dia)

      
            

            credito.save()

            cuota.credit_id = credito

            cuota.save()

            data_credito = model_to_dict(credito)
            data_cuota = model_to_dict(cuota)

            return redirect('financings:detail_credit', credito.id)
        else:
            print(form.errors)
  

    context = {
        'forms': form,
        'forms_cuota':form_cuota,
        'permisos':recorrer_los_permisos_usuario(request),

    }

    return render(request, template_name, context )


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def validar_codigo_seguridad(request):
    # RECUPERAR DE LA SESIÓN, no generar uno nuevo
    codigo_verificar = request.session.get('codigo_migracion')

    if request.method == 'POST':
        data = json.loads(request.body)
        codigo_usuario = data.get('codigo')

        if str(codigo_usuario) == str(codigo_verificar):
            return JsonResponse({'valido': True})
        
        return JsonResponse({'valido': False})
