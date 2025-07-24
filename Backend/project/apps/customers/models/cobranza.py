from django.db import models

# Relacion
from apps.customers.models import CreditCounselor

class Cobranza(models.Model):
    TIPO_COBRANZA_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('normal', 'Normal'),
        ('castigada', 'Castigada'),
        ('judicial', 'Judicial'),
    ]

    TIPO_GESTION_CHOICES = [
        ('llamada', 'Llamada'),
        ('whatsapp', 'WhatsApp'),
        ('visita', 'Visita presencial'),
        ('correo', 'Correo electrónico'),
    ]

    RESULTADO_CHOICES = [
        ('promesa_pago', 'Promesa de pago'),
        ('pago_realizado', 'Pago realizado'),
        ('no_localizado', 'No localizable'),
        ('negativa_pago', 'Negativa de pago'),
    ]

    ESTADO_COBRANZA_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('gestionado', 'Gestionado'),
        ('incumplido', 'Incumplido'),
        ('cerrado', 'Cerrado'),
    ]

    credito = models.ForeignKey('Credito', on_delete=models.CASCADE, related_name='cobranzas')
    asesor_credito = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, null=True, related_name='cobranzas_gestionadas')
    cuota = models.ForeignKey('Cuota', on_delete=models.CASCADE, related_name='gestiones_cobranza')

    tipo_cobranza = models.CharField(max_length=75)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_gestion = models.DateTimeField()

    tipo_gestion = models.CharField(max_length=75)
    resultado = models.CharField(max_length=75, )

    monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_promesa_pago = models.DateField(null=True, blank=True)

    observaciones = models.TextField(blank=True, null=True)

    estado_cobranza = models.CharField(max_length=75, default='pendiente')

    medio_contacto = models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=75)

    def __str__(self):
        return f'Cobranza #{self.id} - {self.credito}'

    class Meta:
        verbose_name = "Cobranza"
        verbose_name_plural = "Cobranzas"
        ordering = ['-fecha_gestion']
