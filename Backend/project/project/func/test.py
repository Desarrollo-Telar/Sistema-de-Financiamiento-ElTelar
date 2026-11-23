import os
import django
from django.utils import timezone

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # <-- Ajusta si tu settings está en otro path
django.setup()

from apps.financings.models import AccountStatement
from apps.customers.models import Customer

if __name__ == "__main__":
    print("Pruebas")


    clientes = Customer.objects.all()
    print(clientes.count())


    for cliente in clientes:

        print(cliente.get_qr())
    