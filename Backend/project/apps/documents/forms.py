# Formulario
from django import forms

# Models
from .models import Document, DocumentAddress, DocumentCustomer, DocumentGuarantee, DocumentOther, DocumentBank



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


class DocumentBankForms(forms.ModelForm):
    class Meta:
        model = DocumentBank
        fields = ['document']
        labels = {'document': 'Documento'}
        widgets = {
            'document': forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
                'name': 'document',
                'accept': '.csv, .txt'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        document = cleaned_data.get('document')

        if not document:
            self.add_error('document', 'Debe adjuntar un archivo.')

        return cleaned_data
