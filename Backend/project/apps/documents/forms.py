# Formulario
from django import forms

# Models
from .models import Document, DocumentAddress, DocumentCustomer, DocumentGuarantee, DocumentOther

class DocumentForms(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'description',
            'document',            
        ]

        labels = {
            'description':'Descripción',
            'document':'Documento',
        }
        widgets = {
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'document':forms.FileInput(attrs={'type':'file','class':'form-control','name':'document','accept':'.pdf, .doc, .docx,.xls,.xlsx,.txt'}),  
        }