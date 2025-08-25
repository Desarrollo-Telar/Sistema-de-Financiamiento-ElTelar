from django.db import models

# Relacion
from apps.customers.models import CreditCounselor
from apps.financings.models import Credit, PaymentPlan
from apps.users.models import User

# FORMATO
from apps.financings.formato import formatear_numero
# TIEMPO
from datetime import datetime

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

    credito = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='cobranzas')
    asesor_credito = models.ForeignKey(CreditCounselor, on_delete=models.SET_NULL, null=True, related_name='cobranzas_gestionadas')
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='gestiones_cobranza')

    tipo_cobranza = models.CharField(max_length=75)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_gestion = models.DateTimeField(null=True, blank=True)
    fecha_seguimiento =  models.DateTimeField(null=True, blank=True)

    tipo_gestion = models.CharField(max_length=75)
    resultado = models.CharField(max_length=75 )

    monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2) # SALDO ACTUAL DE LA CUOTA
    interes_pendiente = models.DecimalField(max_digits=10, decimal_places=2)  # Interes de la cuota, ya si tiene interes acumulado
    mora_pendiente = models.DecimalField(max_digits=10, decimal_places=2)  # Mora de la cuota, ya si tiene mora acumulado
    fecha_limite_cuota = models.DateField(null=True, blank=True) # Obtener la fecha limite de la cuota
    fecha_promesa_pago = models.DateField(null=True, blank=True)

    observaciones = models.TextField(blank=True, null=True)

    estado_cobranza = models.CharField(max_length=75, default='pendiente')

    #medio_contacto = models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=75)
    fecha_actualizacion = models.DateField("Fecha en que se actualizo la cobranza", default=datetime.now, null=True, blank=True)
    count = models.IntegerField(default=0, verbose_name='Contador')

    def f_monto_pendiente(self):
        return formatear_numero(self.monto_pendiente)
    
    def f_interes_pendiente(self):
        return formatear_numero(self.interes_pendiente)
    
    def f_mora_pendiente(self):
        return formatear_numero(self.mora_pendiente)

    def __str__(self):
        return f'Cobranza #{self.id} - {self.credito}'
    
    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        datos_anteriores = {}
        
        if not es_nuevo:
            # Obtener los valores anteriores antes de guardar
            cobranza_anterior = Cobranza.objects.get(pk=self.pk)
            datos_anteriores = self._obtener_datos_serializados(cobranza_anterior)
        
        # Incrementar el contador
        self.count += 1
        super().save(*args, **kwargs)
        
        # Obtener los datos nuevos después de guardar
        datos_nuevos = self._obtener_datos_serializados(self)
        
        # Crear registro de historial
        if not es_nuevo:
            self._crear_registro_historial(datos_anteriores, datos_nuevos, 'modificacion')
        else:
            self._crear_registro_historial({}, datos_nuevos, 'creacion')
    
    def delete(self, *args, **kwargs):
        datos_anteriores = self._obtener_datos_serializados(self)
        super().delete(*args, **kwargs)
        self._crear_registro_historial(datos_anteriores, {}, 'eliminacion')
    
    def _obtener_datos_serializados(self, instancia):
        """Serializa los datos de la cobranza para el historial"""
        return {
            'tipo_cobranza': instancia.tipo_cobranza,
            'fecha_gestion': str(instancia.fecha_gestion) if instancia.fecha_gestion else None,
            'fecha_seguimiento': str(instancia.fecha_seguimiento) if instancia.fecha_seguimiento else None,
            'tipo_gestion': instancia.tipo_gestion,
            'resultado': instancia.resultado,
            'monto_pendiente': str(instancia.monto_pendiente),
            'interes_pendiente': str(instancia.interes_pendiente),
            'mora_pendiente': str(instancia.mora_pendiente),
            'fecha_limite_cuota': str(instancia.fecha_limite_cuota) if instancia.fecha_limite_cuota else None,
            'fecha_promesa_pago': str(instancia.fecha_promesa_pago) if instancia.fecha_promesa_pago else None,
            'observaciones': instancia.observaciones,
            'estado_cobranza': instancia.estado_cobranza,
            'telefono_contacto': instancia.telefono_contacto,
            'count': instancia.count
        }
    
    def _crear_registro_historial(self, datos_anteriores, datos_nuevos, accion):
        """Crea un registro en el historial"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Obtener el usuario actual si existe
        usuario_actual = None
        try:
            from django.contrib.auth import get_user
            usuario_actual = get_user(None)
            if not usuario_actual or usuario_actual.is_anonymous:
                usuario_actual = None
        except:
            pass
        
        HistorialCobranza.objects.create(
            cobranza=self,
            usuario=usuario_actual,
            accion=accion,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos
        )
    
    def restaurar_version(self, historial_id):
        """Restaura una versión específica del historial"""
        try:
            historial = self.historial.get(id=historial_id)
            datos = historial.datos_anteriores if historial.accion == 'eliminacion' else historial.datos_nuevos
            
            # Restaurar los campos
            for campo, valor in datos.items():
                if hasattr(self, campo):
                    setattr(self, campo, valor)
            
            self.save()
            return True
        except HistorialCobranza.DoesNotExist:
            return False

    class Meta:
        verbose_name = "Cobranza"
        verbose_name_plural = "Cobranzas"
        ordering = ['-fecha_gestion']


class HistorialCobranza(models.Model):
    cobranza = models.ForeignKey(Cobranza, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=[
        ('creacion', 'Creación'),
        ('modificacion', 'Modificación'),
        ('eliminacion', 'Eliminación')
    ])
    
    # Campos para almacenar los valores anteriores
    datos_anteriores = models.JSONField(default=dict)
    datos_nuevos = models.JSONField(default=dict)
    
    observaciones_cambio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Historial de Cobranza"
        verbose_name_plural = "Historial de Cobranzas"
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f'Historial #{self.id} - {self.cobranza} - {self.fecha_cambio}'