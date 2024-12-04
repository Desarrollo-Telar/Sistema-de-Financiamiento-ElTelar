from apps.financings.functions_payment import generar
from celery import shared_task
@shared_task
def comparacion():
    generar()