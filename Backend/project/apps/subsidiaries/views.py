from django.shortcuts import render, get_object_or_404, redirect

# Manejo de mensajes
from django.contrib import messages

# Models
from .models import Subsidiary


# LIBRERIAS PARA CRUD
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion


# MENSAJES
from django.contrib import messages


# Create your views here.

@login_required
def view_clasificacion(request):
    template_name = 'sucursal/clasificacion.html'
    sucursales = Subsidiary.objects.filter(activa=True)
    
    if request.session['sucursal_id']:
        return redirect('index')


    context = {
        'sucursales':sucursales

    }
    return render(request, template_name, context)

@login_required
def view_seleccionado(request, id):
    sucursal = Subsidiary.objects.filter(id=id).first()
    if sucursal is None:
        return redirect('sucursal:clasificacion')

    request.session['sucursal_id'] = sucursal.id
    return redirect('index')
