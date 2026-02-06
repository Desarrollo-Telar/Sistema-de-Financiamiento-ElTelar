
from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Models
from apps.financings.models import  AccountStatement,  Credit

# Formulario
from apps.financings.forms import CreditoForms

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados
# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# FUNCION
from .detalle import cuota as cuota_credito

def credito_demandado(request, credit, data):
    
    cuotas = cuota_credito(credit)

    log_user_action(
        request.user,
        'ESTADO JUDICIAL DEL CREDITO', 
        f'El usuario {request.user} ha cambiado el estado del credito, por estado judicial: {credit}',
        request, 'CREDITO', data
    )

    AccountStatement.objects.create(
        credit=credit,
        cuota = cuotas,
        description = 'CREDITO DEMANDADO',
        saldo_pendiente = credit.saldo_actual

    )

@login_required
@permiso_requerido('puede_asignar_estado_judicial')
def cambiar_estado_judicial(request, id):
    template_name = 'financings/credit/ajustes.html'
    credit = Credit.objects.filter(id=id).first()

    if credit is None:
        return redirect('http_404')
    
    data = model_to_dict(credit) # Datos Antes de Actualizar informacion


    if request.method == 'POST':
        form = CreditoForms(request.POST, instance=credit)

        if form.is_valid():
            credito = form.save(commit=False)
            
            if credito.estado_judicial:
                credito_demandado(request, credit, data)

            credito.save()

            return redirect('financings:detail_credit', credit.id)
        else:
            print(form.errors)
    else:
        form = CreditoForms(instance=credit)
    

    context = {
        'forms': form,
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