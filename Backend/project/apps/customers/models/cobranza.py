from django.db import models

# Relacion
from apps.customers.models import CreditCounselor
from apps.financings.models import Credit, PaymentPlan, Recibo
from apps.users.models import User


# FORMATO
from apps.financings.formato import formatear_numero
# TIEMPO
from datetime import datetime, date
from django.utils import timezone

import uuid



class Cobranza(models.Model):
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
    codigo_gestion = models.CharField(max_length=75, null=True, blank=True)


    def get_fecha_seg_o_promesa(self):
        fechas = []

        if self.fecha_seguimiento:
            fechas.append(self.fecha_seguimiento.date())

        if self.fecha_promesa_pago:
            fechas.append(self.fecha_promesa_pago)

        if fechas:
            return max(fechas)

        return None



    def ver_recibo(self):
        obtener_recibo = Recibo.objects.filter(cuota=self.cuota).first()

        if obtener_recibo is None:
            estados_cobranza = ['COMPLETADO', 'INCUMPLIDO']
            
            if self.estado_cobranza in estados_cobranza or self.resultado == 'Pago realizado':
                self.estado_cobranza = 'PENDIENTE'
                self.resultado = 'Promesa de pago'
                self.save()
            return None
        else:
            estados_cobranza = ['PENDIENTE', 'INCUMPLIDO']
            if self.estado_cobranza in estados_cobranza:
                self.resultado = 'Pago realizado'
                self.estado_cobranza = 'COMPLETADO'
                self.save()

        return obtener_recibo.pago.id

    def calcular_dias(self):
        hoy = timezone.now().date()
        dias = None

        if self.estado_cobranza == 'COMPLETADO':
            return dias
        
        fecha = self.get_fecha_seg_o_promesa()

        if not fecha:
            return dias
        

        dias = (fecha - hoy ).days
           
        
        if dias < 0:
            self.resultado = 'Negativa de pago'            
            self.observaciones = 'El cliente no se ha presentado segun lo gestionado.'

            if self.estado_cobranza != 'INCUMPLIDO':
                self.estado_cobranza = 'INCUMPLIDO'
                #self.save()
        else:
            if self.estado_cobranza != 'PENDIENTE':
                self.estado_cobranza = 'PENDIENTE'
                self.resultado = 'Promesa de pago'                
                #self.save()

        return dias

    def f_monto_pendiente(self):
        return formatear_numero(self.monto_pendiente)
    
    def f_interes_pendiente(self):
        return formatear_numero(self.interes_pendiente)
    
    def f_mora_pendiente(self):
        return formatear_numero(self.mora_pendiente)

    def __str__(self):
        return f'Cobranza #{self.id} - {self.credito} - {self.estado_cobranza}'
    
    def _generar_codigo_gestion(self):
        if not self.codigo_gestion:
            codigo_ui = str(uuid.uuid4())[:8]  # Genera un UUID y toma solo 8 caracteres
            codigo_asesor = self.asesor_credito.codigo_asesor
            codigo = f'{codigo_asesor}-{codigo_ui}'
            self.codigo_gestion = codigo
    
    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        datos_anteriores = {}
        
        if not es_nuevo:
            # Obtener los valores anteriores antes de guardar
            cobranza_anterior = Cobranza.objects.get(pk=self.pk)
            datos_anteriores = self._obtener_datos_serializados(cobranza_anterior)
        
        # Incrementar el contador
        self.count += 1
        # creacion de codigo
        self._generar_codigo_gestion()

        if self.estado_cobranza == 'COMPLETADO' or self.resultado == 'Pago realizado':
            if self.cuota.status:
                self.resultado = 'Pago realizado'
                self.estado_cobranza = 'COMPLETADO'
        
        
    

        # guardado
        super().save(*args, **kwargs)
        
        # Obtener los datos nuevos después de guardar
        datos_nuevos = self._obtener_datos_serializados(self)
        
        # Crear registro de historial
        if not es_nuevo:
            self._crear_registro_historial(datos_anteriores, datos_nuevos, 'modificacion')
        else:
            self._crear_registro_historial({}, datos_nuevos, 'creacion')
        
        # Vincula la descripcion al comentario
        if self.observaciones is not None or self.observaciones != '':
            self._crear_comentario()
        sucursal = self.asesor_credito.sucursal
        
        
        
    
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
    
    def _crear_comentario(self):
        from apps.actividades.models import VotacionCredito
        puntuacion = 1

        if self.estado_cobranza == 'COMPLETADO':
            puntuacion = 3
        elif self.estado_cobranza == 'PENDIENTE':
            puntuacion = 2
        else:
            puntuacion = 1


        VotacionCredito.objects.create(
            usuario = self.asesor_credito.usuario,
            credito = self.credito,
            puntuacion = puntuacion,
            comentario = self.observaciones


        )

        


    
    def _crear_registro_historial(self, datos_anteriores, datos_nuevos, accion):
        """Crea un registro en el historial"""
        
        HistorialCobranza.objects.create(
            cobranza=self,
            usuario=self.asesor_credito.usuario,
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
    cobranza = models.ForeignKey(Cobranza, on_delete=models.CASCADE, null=True, blank=True, related_name='historial')
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