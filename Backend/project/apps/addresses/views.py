# URL
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# FORMS
from .forms import AddressForms

# MODELS
from .models import Address
from apps.customers.models import Customer

# CRUD
from django.views.generic import CreateView

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# DECORADORES
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_secretaria, usuario_administrador
from django.utils.decorators import method_decorator

# Create your views here.
# MENSAJES
from django.contrib import messages

# --- CREAR DIRECCION NUEVA --- #
class AddressCreateView(CreateView):
    @method_decorator([usuario_activo])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request,customer_code, *args, **kwargs):
        template_name = 'addresses/address_add.html'
        cliente = get_object_or_404(Customer, customer_code= str(customer_code))
        
        context = {
            'permisos':recorrer_los_permisos_usuario(request),
            'form':AddressForms,            
            'customer_code':cliente.customer_code
        }
        return render(request, template_name, context)

    def post(self, request, customer_code,*args, **kwargs):
        
        cliente = get_object_or_404(Customer, customer_code= str(customer_code))
        form = AddressForms(request.POST)
       

        if form.is_valid():
            direccion = form.save(commit=False)

            direccion.customer_id = cliente

            
            direccion.save()
            
            
            return redirect('customers:detail',cliente.customer_code ) 
          
        else:
            return self.render_to_response(self.get_context_data(form=form))

# --- ACTUALIZAR DIRECION -----
@usuario_activo
@login_required
@usuario_administrador
def addressUpdateView(request, id,customer_code):

    template_name = 'addresses/address_update.html'

    cliente = get_object_or_404(Customer, customer_code= str(customer_code))
    address = get_object_or_404(Address,id=id)

    if request.method == 'POST':
        form = AddressForms(request.POST, instance=address)
        if form.is_valid():
            formulario = form.save(commit=False)

            formulario.save()
            return redirect('customers:detail',cliente.customer_code ) 
       
           

    form = AddressForms(instance=address)

    context = {
        'form':form,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    
    return render(request, template_name, context)

@login_required
@usuario_activo
def crear_municipio(request):
    template_name = 'addresses/created_municipio.html'
    context = {
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)