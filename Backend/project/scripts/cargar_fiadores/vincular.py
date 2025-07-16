
import json

# Modelos
from apps.customers.models import Customer
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome
from apps.financings.models import Guarantees, DetailsGuarantees

# Funcionalidades
from django.db.models import Value, F
from django.db.models.functions import Concat

TIPO_GARANTIA = 'FIADOR'

def especificaciones(codigo_cliente, nombre, lugar_trabajo, ingresos,numero_telefono):
    texto = { 
        "Codigo_de_Cliente": codigo_cliente, 
        "Nombre": nombre, 
        "Lugar_de_Trabajo": lugar_trabajo, 
        "Ingresos": ingresos, 
        "Numero_de_Telefono": numero_telefono, 
        "fotografia": "" 
    }

    return json.dumps(texto)

def buscar_informacion_laboral(cliente):
    informacion_laboral = WorkingInformation.objects.get(customer_id=cliente).first()
    otra_fuente_ingreso = OtherSourcesOfIncome.objects.get(customer_id=cliente).first()

    informacion_ingresos = None
    lugar_trabajo = None

    if informacion_laboral is not None:
        informacion_ingresos = informacion_laboral.f_salary()
        lugar_trabajo = informacion_laboral.company_name
    
    if otra_fuente_ingreso is not None:
        informacion_ingresos = otra_fuente_ingreso.f_salary()
        lugar_trabajo = otra_fuente_ingreso.source_of_income
    
    return informacion_ingresos,lugar_trabajo

def filtro_cliente(nombre_completo):
    customers = Customer.objects.annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'))
    ).filter(full_name__icontains=nombre_completo).first()
    return customers


def filtro_fiador(customers):
    

    if customers is not None:
        ingresos_chamba, lugar_chamba = buscar_informacion_laboral(customers)

        codigo_cliente = customers.customer_code
        nombre = f'{customers.first_name} {customers.last_name}'
        lugar_trabajo = lugar_chamba
        ingresos = ingresos_chamba
        numero_telefono = customers.telephone
        return especificaciones(codigo_cliente, nombre, lugar_trabajo, ingresos, numero_telefono)
    
    return None

def registrar_garantia(cliente, fiador):

    cliente = filtro_cliente(cliente)
    fiadors = filtro_cliente(fiador)

    garantias = Guarantees.objects.filter(credit_id__customer_id=cliente.id)


    for garantia in garantias:
        nuevo_detalle_garantia = DetailsGuarantees.objects.create(
            garantia_id = garantia,
            tipo_garantia = TIPO_GARANTIA,
            especificaciones = filtro_fiador(fiadors),
            valor_cobertura = 0
        )
        print('Registro de Nueva Garantia.')






