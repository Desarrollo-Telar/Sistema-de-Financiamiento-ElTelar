# Formulario
from django import forms
from django.core.exceptions import ValidationError

# Models
from apps.actividades.models import VotacionCliente, VotacionCredito


class VotacionClienteForm(forms.ModelForm):
    puntuacion = forms.IntegerField(
        label="Puntuación (*)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5
        })
    )
    
    comentario = forms.CharField(
        label="Comentario (*)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3'
        })
    )

    class Meta:
        model = VotacionCliente
        fields = ['puntuacion', 'comentario']

    def clean_puntuacion(self):
        puntuacion = self.cleaned_data.get('puntuacion')

        if puntuacion is None:
            raise ValidationError("La puntuación es obligatoria.")

        if not (1 <= puntuacion <= 5):
            raise ValidationError("La puntuación debe estar entre 1 y 5.")

        return puntuacion

class VotacionCreditoForm(forms.ModelForm):
    puntuacion = forms.IntegerField(
        label="Puntuación (*)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5
        })
    )
    
    comentario = forms.CharField(
        label="Comentario (*)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3'
        })
    )

    class Meta:
        model = VotacionCredito
        fields = ['puntuacion', 'comentario']

    def clean_puntuacion(self):
        puntuacion = self.cleaned_data.get('puntuacion')

        if puntuacion is None:
            raise ValidationError("La puntuación es obligatoria.")

        if not (1 <= puntuacion <= 5):
            raise ValidationError("La puntuación debe estar entre 1 y 5.")

        return puntuacion