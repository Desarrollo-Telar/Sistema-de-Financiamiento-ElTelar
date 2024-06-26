from django.db import models

# MODELOS
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan
from apps.users.models import User

# Create your models here.
class Document(models.Model):
    description = models.TextField("Descripción",blank=True, null=True)
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural ="Documentos"

class DocumentCustomer(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE,related_name='customer_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')


    class Meta:
        verbose_name = "Documento de Cliente"
        verbose_name_plural ="Documentos de Clientes"

class DocumentAddress(models.Model):
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address_documents')
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='address_documents')


    class Meta:
        verbose_name = "Documento de dirección"
        verbose_name_plural ="Documentos de Direcciones"

class DocumentGuarantee(models.Model):
    investment_plan_id = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='documents')
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='guarantee_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='guarantee_documents')

    class Meta:
        verbose_name = "Documento de Garantía"
        verbose_name_plural = "Documentos de Garantías"


class DocumentOther(models.Model):
    description = models.CharField("Descripción", max_length=150, blank=True, null=True)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='other_documents')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='other_documents')
    
    
    class Meta:
        verbose_name = "Otro Documento"
        verbose_name_plural = "Otros Documentos"