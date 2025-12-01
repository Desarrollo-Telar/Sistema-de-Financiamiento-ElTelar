from django.db import models

# MODELOS
from apps.customers.models import Customer, Cobranza
from apps.addresses.models import Address
from apps.InvestmentPlan.models import InvestmentPlan
from apps.users.models import User
from apps.financings.models import Banco, DetailsGuarantees
from apps.subsidiaries.models import Subsidiary

# SIGNALS
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver

from project.settings import MEDIA_URL, STATIC_URL
from datetime import timedelta
from project.database_store import minio_client  # asegúrate de que esté importado correctamente

# Create your models here.
class DocumentoCobranza(models.Model):
    cobranza = models.ForeignKey(Cobranza, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='gestion/cobranza/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cobranza.codigo_gestion} {self.cobranza.resultado}'
    
    def get_document(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.archivo.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.archivo)
    
    
    class Meta:
        verbose_name = "Documento Cobranza"
        verbose_name_plural ="Documentos Cobranzas"


class DocumentSistema(models.Model):
    description = models.TextField("Descripción",blank=True, null=True)
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/sistema/')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    def __str__(self):
        return self.description or "Sin Titulo"
    
    def get_document(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.document.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.document)
    
    def titulo(self):
        return self.description

    class Meta:
        verbose_name = "Documento Sistema"
        verbose_name_plural ="Documentos Sistemas"

class DocumentBank(models.Model):
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/banco')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    sucursal = models.ForeignKey(Subsidiary, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.uploaded_at}'

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
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.document.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
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

class DocumentSubsidiary(models.Model):
    ddescription = models.TextField("Descripción",blank=True, null=True)
    document = models.FileField("Documento",blank=True, null=True,upload_to='documents/sucursal/')
    uploaded_at = models.DateTimeField("Fecha de Creación", auto_now_add=True)

    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, related_name='subsidiary_documents')

    def __str__(self):
        return self.description
    
    
    class Meta:
        verbose_name = "Documento de Sucursal"
        verbose_name_plural = "Documentos de Sucursales"

@receiver(post_delete, sender=Document)
def delete_document_files(sender, instance, **kwargs):
    # instance.image es el campo del documento en el modelo de Documentos
    if instance.document:
        instance.document.delete()





from .task import leer_documento

from project.settings import MEDIA_ROOT
import os

from io import BytesIO



def download_from_minio(bucket_name, file_path, local_path):
    """Descarga un archivo de MinIO y lo guarda localmente."""
    minio_client.fget_object(bucket_name, file_path, local_path)
    return local_path

@receiver(post_save, sender=DocumentBank)
def subir(sender, instance, created, **kwargs):
    if created:  # Solo ejecutamos si el documento es nuevo
        
        bucket_name = "asiatrip"  # Cambia al bucket correcto
        file_path = str(instance.document)  # Esto suele ser la clave del objeto en MinIO.
        local_path = f"/tmp/{file_path}"

        try:
            download_from_minio(bucket_name, file_path, local_path)
            file_path = local_path  # Usar la ruta local descargada
            leer_documento(file_path, instance.id, instance.sucursal)
        except Exception as e:
            print(f"Error descargando el archivo de MinIO: {e}")
            return
        
        """
        try:
            response = minio_client.get_object(bucket_name, file_path)
            file_data = BytesIO(response.read())  # Convertir a BytesIO para leerlo
            print(file_data)
            leer_documento(file_data, instance.id)
        except Exception as e:
            print(f"Error al leer documento {instance.id} desde MinIO: {e}")
        """ 


@receiver(pre_delete, sender=DocumentBank)
def eliminar_documento_banco(sender,instance,**kwargs):
    file_path = os.path.join(MEDIA_ROOT, str(instance.document))  
    instance.document.delete()
