from django import forms

# MODELS
from apps.financings.models import PaymentPlan

class PaymentPlanForms(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = [
            #'start_date',
            #'due_date',
            #'fecha_limite',
            #'saldo_pendiente',
            'mora',
            'interest',
        ]
        labels = {
            'start_date':'FECHA DE INICIO',
            'due_date': 'FECHA DE VENCIMIENTO',
            'fecha_limite':'FECHA LIMITE',
            'saldo_pendiente': 'SALDO CAPITAL PENDIENTE',
            'mora': 'MORA A PAGAR',
            'interest': 'INTERES A PAGAR',
        }

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'fecha_limite': forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'saldo_pendiente': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"any"}),
            'mora': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"any"}),
            'interest': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'step':"any"}),
        }
"""
    def save(self, commit=True):
        # Recogemos los datos limpios desde cleaned_data
        cuota = PaymentPlan(
            start_date=self.cleaned_data.get('start_date'),
            due_date=self.cleaned_data.get('due_date'),
            fecha_limite=self.cleaned_data.get('fecha_limite'),
            saldo_pendiente=self.cleaned_data.get('saldo_pendiente'),
            mora=self.cleaned_data.get('mora'),
            interest=self.cleaned_data.get('interest'),
            cambios=True  # Si es un campo por defecto o calculado
        )
        
        # Si se debe guardar inmediatamente
        if commit:
            cuota.save()
        
        return cuota
"""