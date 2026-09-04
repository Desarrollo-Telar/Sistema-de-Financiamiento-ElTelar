# Formulario
from django import forms

# Models
from .models import Document, DocumentAddress, DocumentCustomer, DocumentGuarantee, DocumentoCobranza, DocumentBank
from django.forms.widgets import ClearableFileInput


class DocumentForms(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document']
        labels = {
            'description': 'Título',
            'document': 'Documento',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
                'name': 'document',
                'accept': '.pdf, .doc, .docx, .xls, .xlsx, .txt'
            }),
        }

    # Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        document = cleaned_data.get('document')

        if not description:
            self.add_error('description', 'El título no puede estar vacío.')
        if not document:
            self.add_error('document', 'Debe adjuntar un documento.')

        return cleaned_data



from .models import DocumentBank

class DocumentBankForms(forms.ModelForm):
    # Opciones estáticas para el banco
    BANCO_CHOICES = [
        ('', 'Seleccione un banco'),
        ('BANRURAL', 'BANRURAL'),
        ('BANCO INDUSTRIAL', 'BANCO INDUSTRIAL'),
    ]

    # Sobrescribimos o añadimos el campo con Choices
    nombre_del_banco = forms.ChoiceField(
        choices=BANCO_CHOICES,
        label='Nombre del Banco',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = DocumentBank
        fields = ['document', 'sucursal', 'nombre_del_banco']
        labels = {
            'document': 'Documento',
            'sucursal': 'Sucursal',
            'nombre_del_banco': 'Nombre del Banco',
        }
        widgets = {
            'document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv, .txt'
            }),
            'sucursal': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        document = cleaned_data.get('document')
        sucursal = cleaned_data.get('sucursal')
        nombre_del_banco = cleaned_data.get('nombre_del_banco')

        if not document:
            self.add_error('document', 'Debe adjuntar un archivo.')
        if not sucursal:
            self.add_error('sucursal', 'Debe seleccionar una sucursal.')
        if not nombre_del_banco:
            self.add_error('nombre_del_banco', 'Debe seleccionar un banco.')

        return cleaned_data




