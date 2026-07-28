import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Tiempo
from datetime import datetime,timedelta

# Modelos
from apps.financings.models import Credit, PaymentPlan
from apps.InvestmentPlan.models import InvestmentPlan
from apps.users.models import User  

# DECIMAL
from decimal import Decimal

def cuota_actual(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    siguiente_pago = None

    if credito.is_paid_off:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
        
    else:
        siguiente_pago = PaymentPlan.objects.filter(
            credit_id__id=credito.id,
            start_date__lte=dia,
            fecha_limite__gte=dia_mas_uno
        ).first()

    
    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()

    return siguiente_pago 



if __name__ == '__main__':

    
    contextoA = {
        'modulo': 'Plan de Inversión',
        'id': 1
    }

    contextoB = {
            'modulo': 'Plan de Inversión',
            'id': 1
    }
    contextoC = {
            'modulo': 'Plan de Inversión',
            'id': 2
        }
    contextoD = {
                'modulo': 'Plan de Inversión',
                'id': 2
            }

    notarios_lista = [ contextoA, contextoB, contextoC, contextoD ]

    ids_notarios = [ ]

    for notario in notarios_lista:
        if notario.get('id'):
            ids_notarios.append(notario.get('id'))
            

    ids_unicos = set(ids_notarios)
    

    usando_ids_unicos = User.objects.filter(id__in=ids_unicos)
    
    print(f"Usuarios notarios encontrados: {[user.email for user in usando_ids_unicos]}")

    if len(ids_unicos) == 1:
        # CASO 1: Todos los módulos están asignados al mismo notario (ej. ID 1 y ID 1)
        id_unico = list(ids_unicos)[0]
        try:
            user_notario = User.objects.get(id=id_unico)
            print(f"Enviando correo al notario con ID {id_unico} y correo {user_notario.email}")
        except User.DoesNotExist:
            pass  # Manejo de error si el usuario no existe en la base de datos
            

    else:
        # CASO 2: Los IDs son diferentes, enviamos correos individuales con formatos específicos
        for notario in notarios_lista:
            id_notario = notario.get('id')
            modulo = notario.get('modulo')
            
            if not id_notario or not modulo:
                continue
                
            try:
                user_notario = User.objects.get(id=id_notario)
                
                print(f"Enviando correo al notario con ID {id_notario}, correo {user_notario.email} y módulo {modulo}")
            
            except User.DoesNotExist:
                continue


