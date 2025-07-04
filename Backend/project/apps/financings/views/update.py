from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Payment, PaymentPlan, AccountStatement, Recibo
from apps.financings.models import Invoice

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# FORMULARIO
from apps.financings.forms import PaymentPlanForms, BoletaForm

# Manejo de mensajes
from django.contrib import messages
# Create your views here.

### ---------------- ACTUALIZAR --------------------
@login_required
@permiso_requerido('puede_editar_boleta_pago')
def update_pago(request,id):
    boleta = get_object_or_404(Payment, id=id)

    template_name = 'financings/payment/update.html'

    if request.method == 'POST':
        form = BoletaForm(request.POST, request.FILES, instance=boleta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento Actualizado')
            return redirect('financings:detalle_boleta', boleta.id)

    form = BoletaForm(instance=boleta)
    context = {
        'form':form,
        'title':f'Actualizar el registro de la boleta. {boleta.numero_referencia}',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@login_required
@permiso_requerido('puede_aplicar_descuento_cuota')
def update_cuota(request, id):
    template_name = 'financings/cuota/update.html'
    cuota = get_object_or_404(PaymentPlan, id=id)
    mora_antigua = cuota.mora 
    interes_antiguo = cuota.interest

    if cuota.mora == 0 and cuota.interest == 0:
        messages.error(request, 'No hay cuota por cobrar')
        return redirect('index')

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
                    estado_cuenta.interest_paid = -(interes_antiguo - interes_nuevo)

                if mora_antigua != mora_nueva:
                    print('DESCUENTO APLICADO POR MOROSIDAD')
                    # Si ya había un descuento por interés, lo sumamos con el de mora
                    estado_cuenta.description=f'DESCUENTO APLICADO POR MOROSIDAD '
                    
                    estado_cuenta.late_fee_paid = -(mora_antigua - mora_nueva ) # Restar el monto de mora

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

            messages.success(request,'El descuento fue aplicado')

            return redirect('index')
            
    else:
        form = PaymentPlanForms(instance=cuota)

    context = {
        'form': form,
        'title': f'Aplicacion de Descuento para la cuota. {cuota}',
        'cuota': cuota,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request, template_name, context)


@login_required
@usuario_activo
def generar_factura(request,id):
   
    
    recibo = get_object_or_404(Recibo, id=id)
    print(recibo.factura)
    if not recibo.factura:
        recibo.factura = True
        recibo.save()
    
        factura = Invoice()
        factura.recibo_id = recibo
        factura.save()

        messages.success(request, 'Factura Creada')
    

    return redirect('financings:detail_credit',recibo.pago.credit.id)



