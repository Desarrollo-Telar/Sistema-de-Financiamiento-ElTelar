from django import forms

from .models import Imagen, ImagenAddress, ImagenCustomer, ImagenGuarantee, ImagenOther

class ImagenForms(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = [
            'image',
            'description'
        ]

        labels = {
            'image':'Imagen',
            'description':'Descripción'
        }
        
        widgets = {
            'image':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'image/*'}),  
            'description':forms.TextInput(attrs={'class':'form-control'}),
        }