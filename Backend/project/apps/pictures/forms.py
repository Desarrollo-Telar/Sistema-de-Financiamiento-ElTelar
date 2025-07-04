from django import forms

from .models import Imagen, ImagenAddress, ImagenCustomer, ImagenGuarantee, ImagenOther

class ImagenForms(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = [
            'description',
            'image'
            
        ]

        labels = {
            'image':'Imagen',
            'description':'Titulo'
        }
        
        widgets = {
            'image':forms.FileInput(attrs={'type':'file','class':'form-control','name':'image','accept':'image/*'}),  
            'description':forms.TextInput(attrs={'class':'form-control'}),
        }