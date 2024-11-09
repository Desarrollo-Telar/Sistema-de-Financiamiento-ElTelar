from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.financings.models import Invoice

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# FORMULARIO
from apps.financings.forms import PaymentPlanForms

# Create your views here.

### ---------------- ACTUALIZAR --------------------
@login_required
@usuario_activo
def update_pago(request,id):
    template_name = ''
    pago = get_object_or_404(Payment,id=id)
    context = {
        'title':'ELTELAR'
    }
    return render(request)

@login_required
@usuario_activo
def update_cuota(request, id):
    template_name = 'financings/cuota/update.html'
    cuota = get_object_or_404(PaymentPlan, id=id)
    mora_antigua = cuota.mora 
    interes_antiguo = cuota.interest

    if request.method == 'POST':
        form = PaymentPlanForms(request.POST, instance=cuota)
        if form.is_valid():
            estado_cuenta = AccountStatement()
            estado_cuenta.credit = cuota.credit_id

            interes_nuevo = form.cleaned_data['interest']
            mora_nueva = form.cleaned_data['mora']

            # Si hay cambios en los intereses o mora, registramos un estado de cuenta
            if interes_antiguo != interes_nuevo or mora_antigua != mora_nueva:
                # Descripción del cambio
                if interes_antiguo != interes_nuevo:
                    print('DESCUENTO APLICADO POR INTERES')
                    estado_cuenta.description = f'DESCUENTO APLICADO POR INTERES '
                    estado_cuenta.interest_paid = -interes_nuevo

                if mora_antigua != mora_nueva:
                    print('DESCUENTO APLICADO POR MOROSIDAD')
                    # Si ya había un descuento por interés, lo sumamos con el de mora
                    estado_cuenta.description=f'DESCUENTO APLICADO POR MOROSIDAD '
                    
                    estado_cuenta.late_fee_paid = -mora_nueva  # Restar el monto de mora

                # Si ambos valores cambian, la descripción reflejará ambos descuentos
                if interes_antiguo != interes_nuevo and mora_antigua != mora_nueva:
                    print('DESCUENTOS APLICADOS')
                    estado_cuenta.description = 'DESCUENTOS APLICADOS'

                estado_cuenta.save()  # Guardamos solo una vez el estado de cuenta

            # Actualizamos los valores de la cuota
            cuota.interest = interes_nuevo
            cuota.mora = mora_nueva
            cuota.cambios = True
            cuota.save()

            return redirect('financings:detail_credit',cuota.credit_id.id)
            
    else:
        form = PaymentPlanForms(instance=cuota)

    context = {
        'form': form,
        'title': f'ELTELAR - ACTUALIZACION DE CUOTA',
        'cuota': cuota,
    }

    return render(request, template_name, context)


@login_required
@usuario_activo
def generar_factura(request,id):
    recibo = get_object_or_404(Recibo, id=id)
    recibo.factura = True
    recibo.save()
    """
    factura = Invoice()
    factura.recibo_id = recibo
    factura.save()
    """

    return redirect('financings:detail_credit',recibo.pago.credit.id)



