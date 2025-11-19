# Signals
from django.db.models.signals import pre_save, post_save, post_delete

# Django
from django.dispatch import receiver

# Modelo
from .models import Customer, CreditCounselor, Cobranza
from apps.addresses.models import Municiopio, Departamento
from django.db.models import Q
# Tiempo
from datetime import datetime

# SEND EMAILS
from project.send_mail import send_email_new_customer

# Settings
from django.contrib.sites.models import Site
from django.conf import settings


# QR
from scripts.generadores.generate_qr import generate_qr
from project.database_store import minio_client



# Función para generar el código de cliente basado en el estado y año actual
def generate_customer_code(status, current_year, counter):
    status_suffix = {
        'Posible Cliente': 'S',
        'No Aprobado': 'N',
        'Aprobado': '',
        'Revisión de documentos': 'D',
        'Dar de Baja': 'E',
    }
    suffix = status_suffix.get(status, '')
    return f'{current_year}-{suffix}{counter}'

def is_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False
        
@receiver(pre_save, sender=Customer)
def set_customer_code_and_update_status(sender, instance, **kwargs):
    buscar_asesor = None
    if instance.new_asesor_credito:
        buscar_asesor = CreditCounselor.objects.filter(id=instance.new_asesor_credito.id).first()
        instance.asesor = f'{buscar_asesor.nombre} {buscar_asesor.apellido}'

    

    departamento = instance.lugar_emision_tipo_identificacion_departamento
    municipio = instance.lugar_emision_tipo_identificacion_municipio

    # Filtro condicionalmente por id si es un número
    filtros_departamento = Q(nombre__icontains=departamento)
    if is_int(departamento):
        filtros_departamento |= Q(id=departamento)

    departamento_f = Departamento.objects.filter(filtros_departamento).first()

    filtros_municipio = Q(nombre__icontains=municipio)
    if is_int(municipio):
        filtros_municipio |= Q(id=municipio)

    municipio_f = Municiopio.objects.filter(filtros_municipio).first()

    if departamento_f and municipio_f:
        instance.lugar_emision_tipo_identificacion_departamento = departamento_f.nombre
        instance.lugar_emision_tipo_identificacion_municipio = municipio_f.nombre

    # Si el código del cliente está vacío o es una cadena vacía, genera uno nuevo
    if not instance.customer_code or instance.customer_code == '':
        current_date = datetime.now()
        current_year = current_date.year
        counter = 1
        
        # Generar el código base
        customer_code = generate_customer_code(instance.status, current_year, counter)

        # Verificar si no existe un código igual, si no, generar uno nuevo
        while Customer.objects.filter(customer_code=customer_code).exists():
            counter += 1
            customer_code = generate_customer_code(instance.status, current_year, counter)

        instance.customer_code = customer_code

    # Si el cliente ya existe, verificar si el estado ha cambiado
    elif instance.pk and Customer.objects.filter(pk=instance.pk).exists():
        current_customer = Customer.objects.get(pk=instance.pk)
        if current_customer.status != instance.status:
            current_date = datetime.now()
            current_year = current_date.year
            counter = 1
            
            # Generar el código base
            customer_code = generate_customer_code(instance.status, current_year, counter)

            # Verificar si no existe un código igual, si no, generar uno nuevo
            while Customer.objects.filter(customer_code=customer_code).exists():
                counter += 1
                customer_code = generate_customer_code(instance.status, current_year, counter)

            instance.customer_code = customer_code

def generar_numero_identificacion_sucursal(instance):

    if instance.sucursal is None:
        return None
    
    codigo_sucursal = instance.sucursal.codigo_sucursal if instance.sucursal else 0
    cui = instance.identification_number
    codigo_postal = instance.sucursal.codigo_postal if instance.sucursal.codigo_postal else 0
    contador = 0

    contador = Customer.objects.filter(sucursal = instance.sucursal).count() + 1

    correlativo = str(contador).zfill(4)
    numero_identificacion_sucursal = f'{codigo_sucursal}-{cui}-{correlativo}-{codigo_postal}'
    return numero_identificacion_sucursal

@receiver(post_save, sender=Customer)
def send_message(sender, instance, created, **kwargs):
    customer = instance
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # Verifica si está en HTTPS o HTTP basándose en la configuración
    protocol = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
    
    # Construir la URL completa con el protocolo y el dominio
    filename = f'codigoQr_{customer.customer_code}.png'
    dato = f'https://www.ii-eltelarsa.com/pdf/{customer.id}'
    
    if created:
        generate_qr(dato, filename)
    
    if instance.numero_identificacion_sucursal is None:
        instance.numero_identificacion_sucursal = generar_numero_identificacion_sucursal(instance)
        instance.save()


@receiver(post_delete, sender=Customer)
def delete_image_qr_customer(sender, instance, **kwargs):
    bucket_name = 'asiatrip'
    object_name = f'qr/codigoQr_{instance.customer_code}.png'

    try:
        minio_client.remove_object(bucket_name, object_name)
        print('QR eliminado de MinIO')
    except Exception as e:
        print(f'Error al eliminar QR de MinIO: {str(e)}')

# Notificaciones
from scripts.notificaciones.creacion_notificacion import creacion_notificacion_administrador_secretaria
from apps.actividades.utils import build_notificacion_especificaciones

@receiver(post_save, sender=Cobranza)
def send_notificacion(sender, instance, created, **kwargs):
    es_nuevo = instance.pk is None
    registro = 'registrado'
    if es_nuevo:
        registro = 'actualizado'
        

    sucursal = instance.credito.sucursal
    # Notificacion 
    especificaciones = build_notificacion_especificaciones(
        view_name='financings:detail_credit',
        kwargs={'id': instance.credito.id}    
    )

    mensaje = {
        'title':f'Se ha {registro} la gestion de una cobranza',
        'message':f'El asesor {instance.asesor_credito} ha hecho una gestion de cobranza para el credito {instance.credito}, como resultado en {instance.resultado}',
        'especificaciones':especificaciones
    }

    creacion_notificacion_administrador_secretaria(mensaje,sucursal)