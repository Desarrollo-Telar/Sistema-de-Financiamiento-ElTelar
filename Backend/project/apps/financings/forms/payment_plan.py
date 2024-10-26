from django import forms

# MODELS
from apps.financings.models import PaymentPlan

class PaymentPlanForms(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = [
            
            'saldo_pendiente',
            'mora',
            'interest',
        ]
        labels = {
            
            'saldo_pendiente': 'SALDO CAPITAL PENDIENTE',
            'mora': 'MORA SOBRE INTERES ACUMULADO',
            'interest': 'INTERES ACUMULADO',
        }

        widgets = {
            #'start_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            #'due_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            #'fecha_limite': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'saldo_pendiente': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),
            'mora': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),
            'interest': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),
        }

    
