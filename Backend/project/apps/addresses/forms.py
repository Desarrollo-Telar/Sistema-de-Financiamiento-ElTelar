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
            'type_address'
            
            ]

        labels = {
            'street':'Dirección particular o sede social completa (*)',
            'number':'Zona (*)',
            'city':'Departamento (*)',
            'state':'Municipio (*)',
            
            'country':'País (*)',
            'type_address':'Tipo de direccion (*)',
            'latitud':'Latitud (*)',
            'longitud':'Longitud (*)'
            
            

        }

        
        widgets = {
            'street': forms.TextInput(attrs={'class':'form-control'}),
            'number': forms.TextInput(attrs={'class':'form-control','type':'number','min':'0'}),
            'city': forms.Select(attrs={'class':'form-control city1'}),
            'state': forms.Select(attrs={'class':'form-control state1'}),
            
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'type_address':forms.Select(attrs={'class':'form-control'}),
            'latitud': forms.TextInput(attrs={'class':'form-control'}),
            'longitud': forms.TextInput(attrs={'class':'form-control'}),
           
            

        }

    def __init__(self, *args, **kwargs):
        super(AddressForms, self).__init__(*args, **kwargs)

        self.fields['state'].required = True
        self.fields['city'].required = True
       
        
