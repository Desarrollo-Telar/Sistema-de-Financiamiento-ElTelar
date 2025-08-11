# Formulario
from django import forms

# Models
from apps.actividades.models import DocumentoNotificacionCliente

class DocumentoNotificacionClienteForms(forms.ModelForm):
    class Meta:
        model = DocumentoNotificacionCliente
        fields = ['numero_referencia','description', 'document' ]
        labels = {
            'description': 'Descripción',
            'document': 'Documento (*)',
            'numero_referencia': 'Numero de Referencia del Banco (*)'
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'numero_referencia':forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf, image/*',
                'required': 'required',  # ← Esto es solo visual/HTML
            }),
        }

    # Esta validación sí lo hace obligatorio a nivel de Django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document'].required = True
