# MODELOS
from django.db import models
from apps.customers.models import Customer

from apps.financings.models import Payment, PaymentPlan

# TIEMPO
from django.utils import timezone

# CONVERTIR LOS NUMEROS A LETRAS
from num2words import num2words

# FORMATO
from apps.financings.formato import formatear_numero

class Recibo(models.Model):
    fecha = models.DateField('Fecha De Recibo',default=timezone.now)
    recibo = models.IntegerField("No. Recibo", default=0)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer", blank=True, null=True)
    pago = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="Pago")
    interes = models.DecimalField("Interes",max_digits=12, decimal_places=2, default=0)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora_pagada = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aporte_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    factura = models.BooleanField(default=False)
    cuota = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, null=True, blank=True)

    def recibo_para(self):
        mensaje = ''
       
        if self.pago.acreedor:
            mensaje = f'{self.pago.acreedor.nombre_acreedor}'
        
        if self.pago.seguro:
            mensaje = f'{self.pago.seguro.nombre_acreedor}'
        
        if self.pago.credit:
            mensaje = f'{self.pago.credit.customer_id.get_full_name()} - {self.pago.credit.codigo_credito}'
        
      

        return mensaje


    def Fmora(self):
        return formatear_numero(self.mora)
    
    def Fmonto(self):
        return formatear_numero(self.pago.monto)

    def Fmora_pagada(self):
        return formatear_numero(self.mora_pagada)
    
    def Finteres(self):
        return formatear_numero(self.interes)
    
    def Finteres_pagado(self):
        return formatear_numero(self.interes_pagado)
    
    def Faporte_capital(self):
        return formatear_numero(self.aporte_capital)
    
    def Ftotal(self):
        return formatear_numero(self.total)

    def total_letras(self):
        total = num2words(self.total,lang='es')
        return f'{total} Quetzales'
    
    def interes_pagado_letras(self):
        interes = num2words(self.interes_pagado,lang='es')
        return f'{interes} Quetzales'

    def mora_pagada_letras(self):
        mora = num2words(self.mora_pagada,lang='es')
        return f'{mora} Quetzales'
    
    def aporte_capital_letras(self):
        capital = num2words(self.aporte_capital,lang='es')
        return f'{capital} Quetzales'
    
    def __str__(self):
        mensaje = 'Recibo'
        if self.cuota:
            mensaje += f' - {self.cuota}'
        return mensaje
    
    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'