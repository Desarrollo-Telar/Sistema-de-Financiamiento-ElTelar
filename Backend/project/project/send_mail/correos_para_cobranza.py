from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

# Modelos
from apps.users.models import User
from apps.actividades.models import DetalleInformeCobranza

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

# Notificaciones
from scripts.notificaciones.creacion_notificacion import creacion_notificacion

# URLS
from apps.actividades.utils import build_notificacion_especificaciones

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_recordatorio_cobranza(models):
    template = get_template('email/recordatorio_cobranza.html')
    detalle_informe = DetalleInformeCobranza.objects.filter(cobranza__id = models.id).first()
    full_url = 'https://www.ii-eltelarsa.com'
    
    context = {
        'full_url':full_url,
        'object':models,       
    }

    # Roles por defecto
    roles = ['Administrador', 'Programador']
    asesor_user_id = models.asesor_credito.usuario.id  # Asegúrate que `asesor_credito` esté definido

    usuarios_email = User.objects.filter(
        (
            Q(rol__role_name__in=roles) & Q(status=True)
        ) | Q(id=asesor_user_id)
    ).values_list('email', flat=True).distinct()
        

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'Recordatorio para la gestion de cobranza de: {models.credito}',
        'INVERSIONES INTEGRALES EL TELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')


    if SERVIDOR and usuarios_email: 
        email.send()
