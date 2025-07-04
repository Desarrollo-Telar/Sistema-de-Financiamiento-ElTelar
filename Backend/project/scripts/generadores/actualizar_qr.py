import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# MODELO
from apps.customers.models import Customer

# FUNCION
from .generate_qr import generate_qr



if __name__ == '__main__':
    clientes = Customer.objects.all()

    for customer in clientes:
        print(customer)

        
        filename = f'codigoQr_{customer.customer_code}.png'
        dato = f'https://www.ii-eltelarsa.com/pdf/{customer.id}'

        generate_qr(dato, filename)
        