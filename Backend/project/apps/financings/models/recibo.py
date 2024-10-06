# MODELOS
from django.db import models
from apps.customers.models import Customer

from apps.financings.models import Payment

# TIEMPO
from django.utils import timezone

# CONVERTIR LOS NUMEROS A LETRAS
from num2words import num2words

class Recibo(models.Model):
    fecha = models.DateField('Fecha De Recibo',default=timezone.now)
    recibo = models.IntegerField("No. Recibo", default=0)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    pago = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="Pago")
    interes = models.DecimalField("Interes",max_digits=12, decimal_places=2, default=0)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mora_pagada = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aporte_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    factura = models.BooleanField(default=False)

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