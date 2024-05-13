from django import forms

from .models import Code

class CodeForm(forms.ModelForm):
    
    class Meta:
        model = Code

        fields = [
            'number',

        ]

        labels = {
            'number': 'Codigo de verificacion'
        }


        widgets = {
            'number':forms.TextInput(attrs={'class':'form-control'})
        }
