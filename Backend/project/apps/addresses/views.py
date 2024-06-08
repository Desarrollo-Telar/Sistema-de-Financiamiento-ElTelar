# URL
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# FORMS
from .forms import AddressForms,CoordinateForms

# MODELS
from .models import Address, Coordinate
from apps.customers.models import Customer

# CRUD
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.db.models import Q 

# DECORADORES
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# Create your views here.

class AddressCreateView(CreateView):
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request,customer_code, *args, **kwargs):
        template_name = 'addresses/address_add.html'
        cliente = get_object_or_404(Customer, customer_code= str(customer_code))
        
        context = {
            'title':'ELTELAR - DIRECCIONES',
            'form':CoordinateForms,
            'form2':AddressForms,
            'customer_id':cliente
        }
        return render(request, template_name, context)

    def post(self, request, customer_code,*args, **kwargs):
        
        cliente = get_object_or_404(Customer, customer_code= str(customer_code))
        form = CoordinateForms(request.POST)
        form2 = AddressForms(request.POST)

        if form.is_valid() and form2.is_valid():
            direccion = Address()
            direccion.street = form2.cleaned_data.get('street')
            direccion.number = form2.cleaned_data.get('number')
            direccion.city = form2.cleaned_data.get('city')
            direccion.state = form2.cleaned_data.get('state')
            direccion.postal_code = form2.cleaned_data.get('postal_code')
            direccion.country = form2.cleaned_data.get('country')
            direccion.type_address = form2.cleaned_data.get('type_address')
            direccion.customer_id = cliente
            
            direccion.save()
            coordenada = Coordinate()
            coordenada.latitud = form.cleaned_data.get('latitud')
            coordenada.longitud = form.cleaned_data.get('longitud')
            coordenada.address_id = direccion
            coordenada.save()
            
            return redirect('customers:detail',cliente.customer_code ) 
          
        else:
            return self.render_to_response(self.get_context_data(form=form,form2=form2))

   
    