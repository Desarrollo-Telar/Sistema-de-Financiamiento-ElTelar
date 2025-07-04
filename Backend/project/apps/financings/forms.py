# Formulario
from django import forms

# MODELS
from apps.financings.models import Payment

class PaymentForms(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'credit',
            'disbursement',
            'monto',
            'numero_referencia',
            'estado_transaccion',
            'descripcion',
            'tipo_pago',
            'descripcion_estado'
            
        ]