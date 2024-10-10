# Formulario
from django import forms

# MODELS
from apps.financings.models import PaymentPlan

class PaymentPlanForms(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = [
            'start_date',
            'due_date',
            'fecha_limite',
            'saldo_pendiente',
            'mora',
            'interest',
            

        ]
        labels = {
            'start_date':'FECHA DE INICIO',
            'due_date': 'FECHA DE VENCIMIENTO',
            'fecha_limite':'FECHA LIMITE',
            'saldo_pendiente': 'SALDO CAPITAL PENDIENTE',
            'mora': 'MORA SOBRE INTERES ACUMULADO',
            'interest': 'INTERES ACUMULADO',

        }

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class':'form-control'}),
            'due_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            'fecha_limite':forms.DateTimeInput(attrs={'class':'form-control'}),
            'saldo_pendiente': forms.TextInput(attrs = {'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),
            'mora':forms.TextInput(attrs = {'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),
            'interest':forms.TextInput(attrs = {'class':'form-control', 'type': 'number', 'min': '0', 'step':"0.1"}),

        }