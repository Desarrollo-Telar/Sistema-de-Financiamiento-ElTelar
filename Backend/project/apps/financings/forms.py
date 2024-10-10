# Formulario
from django import forms

# MODELS
from apps.financings.models import Payment

class PaymentForms(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            
        ]