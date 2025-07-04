from django.shortcuts import render, get_object_or_404, redirect

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

# Models
from apps.financings.models import Payment

@login_required
@usuario_activo
def update_payment(request, id):
    pago = get_object_or_404(Payment, id=id)
    template_name = 'financings/payment/create.html'
    context = {
        'title':'EL TELAR - PAGO'
    }
    return render(request, template_name, context)