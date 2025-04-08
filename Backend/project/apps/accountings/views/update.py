from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income
from apps.financings.models import Payment

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion
# Formularios
from apps.accountings.forms import AcreedorForm, SeguroForm, IngresoForm, EgresoForm

# MENSAJES
from django.contrib import messages

@login_required
@usuario_activo
def actualizar_egresos(request, id):
    egreso = get_object_or_404(Egress, id=id)
    template_name = 'contable/create.html'

    if request.method == 'POST':
        form = EgresoForm(request.POST, request.FILES, instance=egreso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento Actualizado')
            return redirect('contable:egresos_detail', egreso.id)

    form = EgresoForm(instance=egreso)
    context = {
        'form':form,
        'title':'ELTELAR'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def actualizar_ingresos(request, id):
    ingreso = get_object_or_404(Income, id=id)
    template_name = 'contable/create.html'

    if request.method == 'POST':
        form = IngresoForm(request.POST, request.FILES, instance=ingreso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento Actualizado')
            return redirect('contable:ingresos_detail', ingreso.id)

    form = IngresoForm(instance=ingreso)
    context = {
        'form':form,
        'title':'ELTELAR'
    }
    return render(request, template_name, context)