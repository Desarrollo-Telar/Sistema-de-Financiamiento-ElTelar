from django import forms

# Models
from .models import Address

class AddressForms(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'street',
            'number',
            'city',
            'state',
            'country',
            'latitud',
            'longitud',
            'type_address',
            
            ]

        labels = {
            'street':'Dirección particular o sede social completa:',
            'number':'Zona',
            'city':'Departamento',
            'state':'Municipio',
            
            'country':'País',
            'type_address':'Tipo de direccion',
            'latitud':'Latitud',
            'longitud':'Longitud'
            
            

        }

        
        widgets = {
            'street': forms.TextInput(attrs={'class':'form-control'}),
            'number': forms.TextInput(attrs={'class':'form-control','type':'number','min':'0'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'type_address':forms.Select(attrs={'class':'form-control'}),
            'latitud': forms.TextInput(attrs={'class':'form-control'}),
            'longitud': forms.TextInput(attrs={'class':'form-control'}),
           
            

        }
        
