from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo


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
    
    if request.method == 'POST':
        form = PaymentPlanForms(request.POST, instance=cuota)
        if form.is_valid():
            form.save()
            return redirect('financings:detail_credit',cuota.credit_id.id)
    else:
        form = PaymentPlanForms(instance=cuota)
    
    context = {
        'form':form,
        'title': f'ELTELAR - ACTUALIZACION DE CUOTA',
        'cuota':cuota,
    }

    return render(request, template_name, context)



