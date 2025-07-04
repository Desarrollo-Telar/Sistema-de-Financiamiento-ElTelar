# URL
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# FORMS
from .forms import ImagenForms

# MODELS
from .models import Imagen, ImagenAddress, ImagenCustomer, ImagenGuarantee, ImagenOther
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan

# CRUD
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.db.models import Q 

# DECORADORES
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Create your views here.

@login_required
@usuario_activo
def create_imagen_customer(request, customer_code):
    template_name = 'pictures/create/create_images_customers.html'
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    if request.method == 'POST':
        form = ImagenForms(request.POST,request.FILES)
        if form.is_valid():
            #imagen = form.save()
             
            imagen = Imagen()
            imagen.image = form.cleaned_data.get('image')
            imagen.description = form.cleaned_data.get('description')
            imagen.save()
            
            imagen_customer = ImagenCustomer(customer_id=customer_id, image_id=imagen)
            imagen_customer.save()
            return redirect('customers:detail',customer_code)
    else:
        form = ImagenForms()
    context = {
        'form': form,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_imagen_customer_address(request,address_id, customer_code):
    template_name = 'pictures/create/create_images_address.html'
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    address_id = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        form = ImagenForms(request.POST,request.FILES)
        if form.is_valid():
            imagen = Imagen()
            imagen.image = form.cleaned_data.get('image')
            imagen.description = form.cleaned_data.get('description')
            imagen.save()
            
            imagen_address = ImagenAddress(address_id=address_id, image_id=imagen, customer_id=customer_id)
            imagen_address.save()


            return redirect('customers:detail',customer_code)
        
    form = ImagenForms
    context = {
        'form': form,
        'address_id':address_id.id,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def create_imagen_customer_guarantee(request,investment_plan_id, customer_code):
    template_name = 'pictures/create/create_images_guarantee.html'
    customer_id = get_object_or_404(Customer, customer_code = customer_code)
    investment_plan_id = get_object_or_404(InvestmentPlan, id=investment_plan_id)
    if request.method == 'POST':
        form = ImagenForms(request.POST,request.FILES)
        if form.is_valid():
            imagen = Imagen()
            imagen.image = form.cleaned_data.get('image')
            imagen.description = form.cleaned_data.get('description')
            imagen.save()
            
            imagen_address = ImagenGuarantee(investment_plan_id=investment_plan_id, image_id=imagen, customer_id=customer_id)
            imagen_address.save()


            return redirect('customers:detail',customer_code)
        
    form = ImagenForms
    context = {
        'form': form,
        'investment_plan_id':investment_plan_id.id,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
@usuario_activo
def delete_imagen(request, id, customer_code):
    imagen = get_object_or_404(Imagen, id=id)
    imagen.delete()
    return redirect('customers:detail', customer_code)


@login_required
@usuario_activo
def update_imagen(request, id, customer_code):
    imagen = get_object_or_404(Imagen, id=id)
    template_name = 'pictures/update/update_images.html'
    print(imagen.image)

    if request.method == 'POST':
        form = ImagenForms(request.POST, request.FILES, instance=imagen)
        if form.is_valid():
            form.save()
            return redirect('customers:detail', customer_code)
    else:
        form = ImagenForms(instance=imagen)

    context = {
        'form':form,
        'imagen_id':id,
        'imagen':imagen,
        'customer_code':customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)
