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

# --- CREAR DIRECCION NUEVA --- #
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
            'customer_code':cliente.customer_code
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

@usuario_activo
@login_required
def addressUpdateView(request, id,customer_code):
    template_name = 'addresses/address_update.html'
    cliente = get_object_or_404(Customer, customer_code= str(customer_code))
    address = get_object_or_404(Address,id=id)
    coordinate = get_object_or_404(Coordinate, address_id=address.id)
    
    if request.method == 'POST':
        form = CoordinateForms(request.POST)
        form2 = AddressForms(request.POST)

        if form.is_valid() and form2.is_valid():
            direccion = address
            direccion.street = form2.cleaned_data.get('street')
            direccion.number = form2.cleaned_data.get('number')
            direccion.city = form2.cleaned_data.get('city')
            direccion.state = form2.cleaned_data.get('state')
            direccion.postal_code = form2.cleaned_data.get('postal_code')
            direccion.country = form2.cleaned_data.get('country')
            direccion.type_address = form2.cleaned_data.get('type_address')
            direccion.customer_id = cliente
                
            direccion.save()
            coordenada = coordinate
            coordenada.latitud = form.cleaned_data.get('latitud')
            coordenada.longitud = form.cleaned_data.get('longitud')
            coordenada.address_id = direccion
            coordenada.save()
                
            return redirect('customers:detail',cliente.customer_code ) 
            
        else:
            return self.render_to_response(self.get_context_data(form=form,form2=form2))
    else:
        initial_data_address = {
            'street':address.street,
            'number':address.number,
            'city':address.city,
            'state':address.state,
            'postal_code':address.postal_code,
            'country':address.country,
            'type_address':address.type_address,
        }
        initial_data_coordinate = {
            'latitud':coordinate.latitud,
            'longitud':coordinate.longitud,

        }

        form2 = AddressForms(initial=initial_data_address)
        form = CoordinateForms(initial=initial_data_coordinate)
        context = {
                'title':'ELTELAR - DIRECCIONES',
                'form':form,
                'form2':form2,
                'customer_code':cliente.customer_code,
                'address_id':id,
        }

        return render(request, template_name, context)