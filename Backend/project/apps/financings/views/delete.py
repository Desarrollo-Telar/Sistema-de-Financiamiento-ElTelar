from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_secretaria, usuario_administrador
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

# Manejo de mensajes
from django.contrib import messages

@login_required
@usuario_activo
@usuario_secretaria
def delete_desembolso(request, id):
    desembolso = get_object_or_404(Disbursement, id=id)
    desembolso.delete()
    return redirect('financings:list_disbursement')


@login_required
@usuario_activo
def delete_credit(request, id):
    credit = get_object_or_404(Credit,id=id)
    credit.delete()
    return redirect('financings:list_credit')