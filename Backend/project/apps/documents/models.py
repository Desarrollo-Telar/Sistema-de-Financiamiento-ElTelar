from django.db import models

# MODELOS
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan
from apps.users.models import User
from apps.financings.models import Banco, DetailsGuarantees

# SIGNALS
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver

from project.settings import MEDIA_URL, STATIC_URL
# Create your models here.

class DocumentBank(models.Model):
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/banco')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    
    def __str__(self):
        return self.document

    class Meta:
        verbose_name = "Documeto de Banco"
        verbose_name_plural ="Documentos de Bancos"

class Document(models.Model):
    description = models.TextField("Descripción",blank=True, null=True)
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return self.description or "Sin Titulo"
    
    def get_document(self):
        return '{}{}'.format(MEDIA_URL,self.document)
    
    def titulo(self):
        return self.description

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural ="Documentos"

class DocumentCustomer(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE,related_name='customer_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f'Documento del Cliente: {self.document_id}'
    
    def titulo(self):
        return self.document_id

    class Meta:
        verbose_name = "Documento de Cliente"
        verbose_name_plural ="Documentos de Clientes"

class DocumentAddress(models.Model):
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address_documents')
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='address_documents')

    def __str__(self):
        return self.document_id.description


    class Meta:
        verbose_name = "Documento de dirección"
        verbose_name_plural ="Documentos de Direcciones"

class DocumentGuarantee(models.Model):
    investment_plan_id = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='documents', blank=True, null=True)
    garantia = models.ForeignKey(DetailsGuarantees, on_delete=models.CASCADE, related_name="guarantee_documents", blank=True,null=True)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='guarantee_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='guarantee_documents',blank=True,null=True)

    def __str__(self):
        return self.document_id.description

    class Meta:
        verbose_name = "Documento de Garantía"
        verbose_name_plural = "Documentos de Garantías"


class DocumentOther(models.Model):
    description = models.CharField("Descripción", max_length=150, blank=True, null=True)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='other_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='other_documents')

    def __str__(self):
        return self.description
    
    
    class Meta:
        verbose_name = "Otro Documento"
        verbose_name_plural = "Otros Documentos"

@receiver(post_delete, sender=Document)
def delete_document_files(sender, instance, **kwargs):
    # instance.image es el campo del documento en el modelo de Documentos
    if instance.document:
        instance.document.delete()





from .task import leer_documento

from project.settings import MEDIA_ROOT
import os


@receiver(post_save, sender=DocumentBank)
def subir(sender, instance, created, **kwargs):
    if created:  # Solo ejecutamos si el documento es nuevo
        file_path = os.path.join(MEDIA_ROOT, str(instance.document))     
        leer_documento(file_path,instance.id)
"""  

@receiver(pre_delete, sender=DocumentBank)
def eliminar_documento_banco(sender,instance,**kwargs):
    file_path = os.path.join(MEDIA_ROOT, str(instance.document))  
    instance.document.delete()
"""