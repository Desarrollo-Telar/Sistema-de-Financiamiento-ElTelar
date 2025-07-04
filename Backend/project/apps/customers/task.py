from celery import shared_task

# EMAILS
from project.send_mail import send_email_new_customer

import logging
logger = logging.getLogger(__name__)

@shared_task
def nuevo_cliente(customer):
    send_email_new_customer(customer)