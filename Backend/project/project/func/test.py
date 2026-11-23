import os
import django
from django.utils import timezone

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # <-- Ajusta si tu settings está en otro path
django.setup()

from apps.financings.models import AccountStatement
from apps.customers.models import Customer

from scripts.generadores.generate_qr import generate_qr_servidor

if __name__ == "__main__":
    print("Pruebas")


    clientes = Customer.objects.all()
    print(clientes.count())

    codigos_clientes = [
        '2026-200',
        '2026-202',
        '2026-201'
    ]


    for cliente in clientes:

        if cliente.customer_code in codigos_clientes:
            filename = f'codigoQr_{cliente.customer_code}.png'
            dato = f'https://www.ii-eltelarsa.com/pdf/{cliente.id}'

            generate_qr_servidor(dato, filename)
    