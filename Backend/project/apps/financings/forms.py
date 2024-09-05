# Formulario
from django import forms

# MODELS
from .models import Payment

class PaymentForms(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            
        ]