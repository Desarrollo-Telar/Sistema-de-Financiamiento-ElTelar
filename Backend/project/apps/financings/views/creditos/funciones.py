from apps.codes.models import Code, User

import random, uuid

from project.send_mail import send_email_code_verification

from django.db.models import Q



def generar_codigo_seguridad(usuario_regis, accion):
    # random.choices devuelve una lista, .join la une en un string
    num = "".join(random.choices('0123456789', k=5)) 
    roles = ['Administrador' ,'Programador']
    
    usuarios = User.objects.filter(Q(rol__role_name__in=roles), status=True)

    for usuario in usuarios:
        send_email_code_verification(usuario, num, usuario_regis, accion)
    print(num)
    
    return num 