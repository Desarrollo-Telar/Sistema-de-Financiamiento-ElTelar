
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Models
from apps.financings.models import  AccountStatement,  Credit, PaymentPlan
from apps.actividades.models import ModelHistory
# Formulario
from apps.financings.forms import CreditoForms, PaymentPlanForms

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados
# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# FUNCION
from .detalle import cuota as cuota_credito, cuota_siguiente

def credito_reesctructurado(request, credit, data, despues):
    
    cuotas = cuota_credito(credit)
    cambios = cambios_realizados(data, despues)

    log_user_action(
        request.user,
        'REESTRUCTURACION DEL CREDITO', 
        f'El usuario {request.user} ha cambiado el estado del credito, por estado judicial: {credit}',
        request, 'CREDITO', data
    )

    AccountStatement.objects.create(
        credit=credit,
        cuota = cuotas,
        description = 'REESTRUCTURACION DEL CREDITO',
        saldo_pendiente = credit.saldo_actual

    )

    ModelHistory.objects.create(
        content_type = 'financings.Credit',
        object_id = credit.id,
        action ='update',
        data = data,
        changes = cambios,
        user = request.user
    )

@login_required
@permiso_requerido('puede_asignar_estado_judicial')
def cambiar_estado_judicial(request, id):
    template_name = 'financings/credit/ajustes.html'
    credit = Credit.objects.filter(id=id).first()

    if credit is None:
        return redirect('http_404')
    
    data = model_to_dict(credit) # Datos Antes de Actualizar informacion
    cuotas = cuota_credito(credit)

    fecha_inicio = credit.fecha_inicio
    tasa_interes = credit.tasa_interes
    plazo = credit.plazo

    saldo_capital = cuotas.saldo_pendiente
    interes = cuotas.interest
    mora = cuotas.mora


    if request.method == 'POST':
        form = CreditoForms(request.POST, instance=credit)
        form_cuota = PaymentPlanForms(request.POST, instance=cuotas)

        if form.is_valid() and form_cuota.is_valid():
            credito = form.save(commit=False)
            cuota = form_cuota.save(commit=False)

            cuota_saldo_capital = cuota.saldo_pendiente
            cuota_interes = cuota.interest
            cuota_mora = cuota.mora
            proxima_cuota = None

            if saldo_capital != cuota_saldo_capital or interes != cuota_interes or mora != cuota_mora:
                proxima_cuota = cuota_siguiente(credit)


            if fecha_inicio != credito.fecha_inicio or tasa_interes != credito.tasa_interes or plazo != credito.plazo:
                
                nuevo_dia = credito.fecha_inicio.day
                cuota.original_day = nuevo_dia
    
                try:
                    cuota.start_date = cuota.start_date.replace(day=nuevo_dia)
                except ValueError:
                    
                    import calendar
                    ultimo_dia = calendar.monthrange(cuota.start_date.year, cuota.start_date.month)[1]
                    cuota.start_date = cuota.start_date.replace(day=ultimo_dia)

                proxima_cuota = cuota_siguiente(credit)
            
            if proxima_cuota is not None:
                proxima_cuota.delete()
                

            data_despues = model_to_dict(credito)
            credito_reesctructurado(request, credit, data, data_despues)
            
            
            cuota.save()
            credito.save()

            return redirect('financings:detail_credit', credit.id)
        else:
            print(form.errors)
    else:
        form = CreditoForms(instance=credit)
        form_cuota = PaymentPlanForms(instance=cuotas)
    

    context = {
        'forms': form,
        'forms_cuota':form_cuota,
        'permisos':recorrer_los_permisos_usuario(request),

    }

    return render(request, template_name, context )

@login_required
@permiso_requerido('puede_asignar_estado_judicial')
def cambiar_estado_judicial_false(request, id):
    credit = Credit.objects.filter(id=id).get()
    data = model_to_dict(credit)

    if credit is None:
        return redirect('http_404')
    
    credit.estado_judicial = False
    credit.save()

    log_user_action(
        request.user,
        'ESTADO JUDICIAL DEL CREDITO', 
        f'El usuario {request.user} ha cambiado el estado del credito judicial: {credit}',
        request, 'CREDITO', data
    )

    return redirect('financings:detail_credit', credit.id)